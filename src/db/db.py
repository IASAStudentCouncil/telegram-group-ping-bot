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
            db (MDB): The MongoDB database reference.
            id (int): The unique identifier for the user, typically the user's Telegram ID.
            username (str | None): The user's Telegram username.
            first_name (str): The user's Telegram first name.
            language (str): The user's preferred language for interaction.
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
        self.id = user_id
        self.username = username
        self.first_name = first_name
        self._default_language = "uk" if language_code in ["uk", "ru"] else "en"
        self.language: Optional[str] = None

        asyncio.create_task(self.__ensure_index())

    async def __ensure_index(self) -> None:
        """Ensures that an index exists on the '_id' field for faster lookups."""
        await self._collection.create_index([("_id", ASCENDING)])

    async def validation(self) -> None:
        """Checks if the user exists in the database and updates or inserts data as necessary."""
        user_data = await self._collection.find_one({"_id": self.id})
        if user_data is None:
            await self._collection.insert_one(
                {
                    "_id": self.id,
                    "username": self.username,
                    "first_name": self.first_name,
                    "language": self._default_language
                }
            )
            self.language = self._default_language
        else:
            fields_to_check = ["username", "first_name"]
            updates = {field: getattr(self, field) for field in fields_to_check if
                       user_data[field] != getattr(self, field)}
            if updates:
                await self._collection.update_one(
                    {"_id": self.id},
                    {"$set": updates}
                )
            self.language = user_data["language"]

    async def change_language(self, language_code: str) -> None:
        """
            Updates the user's preferred language in the database if it has changed.
            Args:
                language_code (str): New language code to be updated.
        """
        if self.language != language_code:
            await self._collection.update_one(
                {"_id": self.id},
                {"$set": {"language": language_code}}
            )
            self.language = language_code


class Group:
    """
        This class simplifies interactions with the 'groups' collection in the database. It handles operations
        such as validating existing group data, updating users, and managing subgroups.
        Attributes:
            db (MDB): The MongoDB database reference.
            id (int): The unique identifier for the group, typically the group's Telegram ID.
            language (str): The group's default language for communication.
    """

    def __init__(self, db: MDB, group_id: int):
        """
            Initializes a Group object for managing group data in the database.
            Args:
                db (MDB): The database connection.
                group_id (int): Unique identifier for the group.
        """
        self._db = db
        self._collection = self._db["groups"]
        self.id = group_id
        self.language: Optional[str] = None

        asyncio.create_task(self.__ensure_index())

    async def __ensure_index(self) -> None:
        """Ensures that an index exists on the '_id' field for faster lookups."""
        await self._collection.create_index([("_id", ASCENDING)])

    async def add_to_db(self) -> None:
        """Inserts a new group into the database."""
        await self._collection.insert_one(
            {
                "_id": self.id,
                "users": [],
                "language": self.language
            }
        )

    async def validation(self) -> None:
        """
            Validates the group's existence in the database. If the group exists, its language is retrieved.
            If the group does not exist, it is added to the database with the default language set to "en".
        """
        group_data = await self._collection.find_one({"_id": self.id}, {"language": 1, "_id": 0})
        self.language = group_data["language"] if group_data else "en"
        if not group_data:
            await self.add_to_db()

    async def delete_from_db(self) -> None:
        """Deletes the group from the database."""
        await self._collection.delete_one({"_id": self.id})

    async def change_language(self, language_code: str) -> None:
        """
            Updates the group's preferred language in the database if it has changed.
            Args:
                language_code (str): New language code to be updated.
        """
        if self.language != language_code:
            self.language = language_code
            await self._collection.update_one(
                {"_id": self.id},
                {"$set": {"language": self.language}}
            )

    async def add_user(self, user_id: int, can_be_pinged: bool = True) -> None:
        """
            Adds a new user to the group with the specified ping permissions.
            Args:
                user_id (int): The user's Telegram ID.
                can_be_pinged (bool): Indicates if the user can be pinged. Defaults to True.
        """
        await self._collection.update_one(
            {"_id": self.id, "users.user_id": {"$ne": user_id}},
            {
                "$push": {
                    "users": {
                        "user_id": user_id,
                        "can_be_pinged": can_be_pinged
                    }
                }
            },
            upsert=True
        )

    async def user_validation(self, user_id: int):
        """
            Validates if a user exists in the group. If not, adds the user to the group.
            Args:
                user_id (int): The user's Telegram ID.
        """
        user_exists = await self._collection.find_one(
            {"_id": self.id, "users.user_id": user_id},
            {"users.user_id": 1, "_id": 0}
        )

        if not user_exists:
            await self.add_user(user_id)

    async def delete_user(self, user_id: int) -> None:
        """
            Removes a user from the group.
            Args:
                user_id (int): The user's Telegram ID.
        """
        await self._collection.update_one(
            {"_id": self.id},
            {
                "$pull": {
                    "users": {"user_id": user_id}
                }
            }
        )

    async def update_user_ping_permission(self, user_id: int, allowed_to_be_pinged: bool = True) -> None:
        """
            Updates the pinging permission for a specified user in the group.
            Args:
                user_id (int): The unique Telegram ID of the user.
                allowed_to_be_pinged (bool): Indicates whether the user is allowed to be pinged.
                                             Defaults to True (allowed).
        """
        await self._collection.update_one(
            {"_id": self.id, "users.user_id": user_id},
            {
                "$set": {
                    "users.$.can_be_pinged": allowed_to_be_pinged
                }
            }
        )

    async def get_user_ids(self, only_pingable: bool = False) -> List[str]:
        """
            Retrieves a list of user IDs in the group, with an option to filter by ping permission.
            Args:
                only_pingable (bool): If True, return only the IDs of users who can be pinged. Defaults to False.
            Returns:
                List[str]: A list of user IDs for users in the group.
        """
        all_user_data = await self.get_all_user_data()
        return [user[0] for user in all_user_data if not only_pingable or user[3]]

    async def get_all_user_data(self) -> List[List[Optional[str]]]:
        """
            Retrieves all user records from the group, including their `first_name`, `username`, and `can_be_pinged` status.
            Returns:
                List[List[Optional[str]]]: A list of lists where each sublist contains the `first_name`, `username`, and `can_be_pinged` status of a user.
        """
        group_data = await self._collection.find_one(
            {"_id": self.id},
            {"users.user_id": 1, "users.can_be_pinged": 1, "_id": 0}
        )
        if not group_data:
            return []

        users_info = group_data.get("users", [])

        user_ids = [user["user_id"] for user in users_info]
        can_be_pinged_map = {user["user_id"]: user["can_be_pinged"] for user in users_info}

        user_collection = self._db["users"]
        users_data = await user_collection.find(
            {"_id": {"$in": user_ids}},
            {"_id": 1, "username": 1, "first_name": 1}
        ).to_list(length=None)

        result = [
            [
                user["_id"],
                user["username"],
                user["first_name"],
                can_be_pinged_map.get(user["_id"])
            ]
            for user in users_data
        ]

        return result


__all__ = ("connect_to_mongo", "setup_database", "User", "Group")
