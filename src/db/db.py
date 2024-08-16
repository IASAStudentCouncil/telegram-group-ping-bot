import logging

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

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
        logging.info("Connected to Mongo client.")
    except ServerSelectionTimeoutError:
        logging.error("Failed to connect to MongoDB: Server selection timeout.")
        raise
    except OperationFailure:
        logging.error("Failed to connect to MongoDB: Authentication failure.")
        raise
    except Exception as e:
        logging.error("An unexpected error occurred while connecting to MongoDB.")
        logging.exception(e)
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
    logging.info(f"Connected to the '{db_name}' database.")

    collections = {
        "users": user_validator,
        "groups": group_validator,
    }
    actual_db_collections = await db.list_collection_names()

    for collection_name, validator in collections.items():
        if collection_name not in actual_db_collections:
            try:
                await db.create_collection(collection_name)
                logging.info(f"Collection '{collection_name}' created successfully.")
            except Exception as e:
                logging.error(f"Error creating collection '{collection_name}'.")
                logging.exception(e)
                raise
        try:
            await db.command("collMod", collection_name, validator=validator)
            logging.info(f"Validator set for collection '{collection_name}'.")
        except Exception as e:
            logging.error(f"Error setting validator for collection '{collection_name}'.")
            logging.exception(e)
            raise

    return db


class User:
    """
    This class simplifies interactions with the 'users' collection in the database. It handles operations
    such as validating existing user data, updating usernames, and changing user language preferences.

    Attributes:
        db (MDB): Reference to the MongoDB database.
        _id (int): Unique identifier for the user, typically the user's Telegram ID.
        username (str): User's Telegram username.
        language (str): User's preferred language, used to localize responses.
    """

    def __init__(self, db: MDB, user_id: int, username: str, language_code: str = "en") -> None:
        """
        Initializes a User object for managing user data in the database.

        Args:
            db (MDB): The database connection.
            user_id (int): Unique telegram identifier for the user.
            username (str): Username of the user.
            language_code (str): Preferred language of the user, defaults to English.
        """

        self.collection = db["users"]
        self._id = user_id
        self.username = username
        self.language = "uk" if language_code in ["uk", "ru"] else "en"

    async def user_validation(self) -> None:
        """
        Checks if the user exists in the database and updates or inserts data as necessary.
        """
        user = await self.collection.find_one({"_id": self._id})
        if user is None:
            await self.collection.insert_one(
                {
                    "_id": self._id,
                    "username": self.username,
                    "language": self.language
                }
            )
        else:
            self.language = user["language"]
            if user["username"] != self.username:
                await self.collection.update_one(
                    {"_id": self._id},
                    {"$set": {"username": self.username}}
                )

    async def change_language(self, language_code: str) -> None:
        """
        Updates the user's preferred language in the database if it has changed.

        Args:
            language_code (str): New language code to be updated.
        """

        if language_code != self.language:
            self.language = language_code
            await self.collection.update_one(
                {"_id": self._id},
                {"$set": {"language": self.language}}
            )


__all__ = ("connect_to_mongo", "setup_database", "User")
