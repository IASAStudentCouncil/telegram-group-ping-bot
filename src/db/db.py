import asyncio
import logging
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError
from pymongo import ASCENDING

from src.config import mongo_uri, db_name
from .schema_validators import *


async def connect_to_mongo(uri: str = mongo_uri) -> AsyncIOMotorClient:
    """
        Connects to MongoDB and confirms the connection is working using a ping command.
        Args:
            uri (str): Connection string for MongoDB.
        Returns:
            AsyncIOMotorClient: A MongoDB client for asynchronous operations.
        Raises:
            ServerSelectionTimeoutError: If the server can't be reached within the timeout.
            OperationFailure: If there's an issue with MongoDB authentication.
            Exception: For other unexpected issues during connection.
    """

    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)

    try:
        await client.admin.command('ping')
        logging.info("Connected to Mongo client")
    except ServerSelectionTimeoutError:
        logging.error("Failed to connect to MongoDB: Server selection timeout")
        client.close()
        raise
    except OperationFailure:
        logging.error("Failed to connect to MongoDB: Authentication failure")
        client.close()
        raise
    except Exception as e:
        logging.error("An unexpected error occurred while connecting to MongoDB")
        logging.exception("Error details:", exc_info=e)
        client.close()
        raise

    return client


async def setup_database(client: AsyncIOMotorClient) -> MDB:
    """
        Sets up required collections and validation rules in the MongoDB database.
        Args:
            client (AsyncIOMotorClient): Client used to access the database.
        Returns:
            MDB: Configured database with necessary collections.
        It checks for required collections and creates them if they are missing, applying validation rules.
    """

    db = client[db_name]
    logging.info(f"Connected to the '{db_name}' database")

    collections = {
        "users": user_validator,
        "groups": group_validator,
    }
    actual_db_collections = await db.list_collection_names()

    for collection_name, validator in collections.items():
        if collection_name not in actual_db_collections:
            try:
                await db.create_collection(collection_name)
                logging.info(f"Collection '{collection_name}' created successfully")
            except Exception as e:
                logging.error(f"Error creating collection '{collection_name}'")
                logging.exception("Error details:", exc_info=e)
                client.close()
                raise
        try:
            await db.command("collMod", collection_name, validator=validator)
            logging.info(f"Validator set for collection '{collection_name}'")
        except Exception as e:
            logging.error(f"Error setting validator for collection '{collection_name}'.")
            logging.exception("Error details:", exc_info=e)
            client.close()
            raise

    return db


class User:
    """
        This class simplifies interactions with the 'users' collection in the database. It handles operations
        such as validating existing user data, updating usernames, and changing user language preferences.
        Attributes:
            db (MDB): Reference to the MongoDB database.
            _id (int): Unique identifier for the user, typically the user's Telegram ID.
            username (str | None): User's Telegram username.
            first_name (str): User's Telegram first name.
            language (str): User's preferred language, used to localize responses.
    """

    def __init__(self, db: MDB, user_id: int, username: str | None, first_name: str, language_code: str = "en") -> None:
        """
            Initializes a User object for managing user data in the database.
            Args:
                db (MDB): The database connection.
                user_id (int): Unique telegram identifier for the user.
                username (str | None): Username of the user.
                first_name (str): First name.
                language_code (str): Default language of the user, defaults to English.
        """

        self._collection = db["users"]
        self._id = user_id
        self.username = username
        self.first_name = first_name
        self._default_language = "uk" if language_code in ["uk", "ru"] else "en"
        self.language: Optional[str] = None

        asyncio.create_task(self.__ensure_index())

    async def __ensure_index(self) -> None:
        """Ensures that an index exists on the '_id' field for faster lookups."""
        await self._collection.create_index([("_id", ASCENDING)])

    async def user_validation(self) -> None:
        """Checks if the user exists in the database and updates or inserts data as necessary."""
        user_data = await self._collection.find_one({"_id": self._id})
        if user_data is None:
            await self._collection.insert_one(
                {
                    "_id": self._id,
                    "username": self.username,
                    "first_name": self.first_name,
                    "language": self._default_language
                }
            )
            self.language = self._default_language
        else:
            fields_to_check = ["username", "first_name"]
            updates = {}
            for field in fields_to_check:
                if user_data[field] != getattr(self, field):
                    updates[field] = getattr(self, field)
            if updates:
                await self._collection.update_one(
                    {"_id": self._id},
                    {"$set": updates}
                )
            self.language = user_data["language"]

    async def change_user_language(self, language_code: str) -> None:
        """
            Updates the user's preferred language in the database if it has changed.
            Args:
                language_code (str): New language code to be updated.
        """
        if self.language != language_code:
            await self._collection.update_one(
                {"_id": self._id},
                {"$set": {"language": language_code}}
            )
            self.language = language_code


class Group:
    """
        This class simplifies interactions with the 'groups' collection in the database. It handles operations
        such as validating existing group data, updating users, and managing subgroups.

        Attributes:
            db (MDB): Reference to the MongoDB database.
            _id (int): Unique identifier for the group, typically the group's Telegram ID.
            users (List[dict]): A list of users within the group.
            language (str): The group's default language, used for communication within the group.
    """

    def __init__(self, db: MDB, group_id: int):
        """
            Initializes a Group object for managing group data in the database.

            Args:
                db (MDB): The database connection.
                group_id (int): Unique identifier for the group.
        """

        self._collection = db["groups"]
        self._id = group_id
        self.users: List[dict] = []
        self.language: Optional[str] = None

        asyncio.create_task(self.__ensure_index())

    async def __ensure_index(self) -> None:
        """Ensures that an index exists on the '_id' field for faster lookups."""
        await self._collection.create_index([("_id", ASCENDING)])

    async def add_group_to_db(self) -> None:
        self.language = "en"
        await self._collection.insert_one(
            {
                "_id": self._id,
                "users": self.users,
                "language": self.language
            }
        )

    async def delete_group_from_db(self) -> None:
        await self._collection.delete_one({"_id": self._id})

    async def change_group_language(self, language_code: str) -> None:
        """
            Updates the group's preferred language in the database if it has changed.

            Args:
                language_code (str): New language code to be updated.
        """

        if self.language != language_code:
            self.language = language_code
            await self._collection.update_one(
                {"_id": self._id},
                {"$set": {"language": self.language}}
            )

    async def add_user(self, user: User) -> None:
        pass

    async def delete_user(self, user: User) -> None:
        pass

    async def allow_to_ping_user(self, user: User) -> None:
        pass

    async def forbide_user_pinging(self, user: User) -> None:
        pass

    async def get_all_usernames(self) -> List[str]:
        pass

    async def get_all_users(self) -> List[dict]:
        pass


__all__ = ("connect_to_mongo", "setup_database", "User", "Group")
