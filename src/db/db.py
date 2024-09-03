import logging
from contextlib import suppress
from typing import List, Optional, Dict

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError, DuplicateKeyError
from pymongo import IndexModel, ASCENDING, TEXT

from src.config import mongo_uri, db_name
from .schema_validators import SchemaValidators


async def connect_to_mongo(uri: str = mongo_uri) -> AsyncIOMotorClient:
    """
        Connects to MongoDB and confirms the connection is working using a ping command.
        Args:
            uri (str): MongoDB connection string.
        Returns:
            AsyncIOMotorClient: MongoDB client for async operations.
        Raises:
            ServerSelectionTimeoutError, OperationFailure, Exception: On connection issues.
    """
    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    try:
        await client.admin.command('ping')
        logging.info("Connected to MongoDB")
    except (ServerSelectionTimeoutError, OperationFailure, Exception) as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        client.close()
        raise
    return client


async def setup_database(client: AsyncIOMotorClient) -> MDB:
    """
        Sets up the database, ensuring collections, validation rules, and indexes are in place.
        Args:
            client (AsyncIOMotorClient): MongoDB client.
        Returns:
            MDB: Configured database.
    """
    db = client[db_name]
    logging.info(f"Connected to the '{db_name}' database")

    collections = {"users": SchemaValidators.USER_VALIDATOR, "groups": SchemaValidators.GROUP_VALIDATOR}
    indexes = {
        "users": [IndexModel([("_id", ASCENDING)])],
        "groups": [
            IndexModel([("_id", ASCENDING)]),
            IndexModel([("users.user_id", ASCENDING)]),
            IndexModel([("custom_tags.name", TEXT)]),
            IndexModel([("custom_tags.user_ids", ASCENDING)])
        ]
    }
    actual_db_collections = await db.list_collection_names()

    for collection_name, validator in collections.items():
        if collection_name not in actual_db_collections:
            await db.create_collection(collection_name)
            logging.info(f"Collection '{collection_name}' created successfully")
            await db.command("collMod", collection_name, validator=validator)
            logging.info(f"Validator set for collection '{collection_name}'")
            try:
                await db[collection_name].create_indexes(indexes[collection_name])
                logging.info(f"Indexes created successfully for '{collection_name}' collections")
            except Exception as e:
                logging.error(f"Error creating indexes: {e}")
    return db


class User:
    """
        Manages user data in the 'users' collection.
        Attributes:
            id (int): User's unique Telegram ID.
            language (str): User's preferred language.
    """

    def __init__(self, db: MDB, user_id: int, language_code: str = "en") -> None:
        """
            Initializes a User object for managing user data in the database.
            Args:
                db (MDB): The database connection.
                user_id (int): Unique telegram identifier for the user.
                language_code (str): Default language of the user, defaults to English.
        """
        self._collection = db["users"]
        self.id = user_id
        self._default_language = "uk" if language_code in ["uk", "ru"] else "en"
        self.language: Optional[str] = None

    async def validation(self) -> None:
        """Validates user data, inserting if not found."""
        try:
            user_data = await self._collection.find_one({"_id": self.id})
            if user_data is None:
                self.language = self._default_language
                await self._collection.insert_one({"_id": self.id, "language": self.language})
            else:
                self.language = user_data["language"]
        except Exception as e:
            logging.error(f"Error validating user {self.id}: {e}")

    async def change_language(self, language_code: str) -> None:
        """Updates user's preferred language."""
        if self.language != language_code:
            try:
                await self._collection.update_one({"_id": self.id}, {"$set": {"language": language_code}})
                self.language = language_code
            except Exception as e:
                logging.error(f"Error changing language for user {self.id}: {e}")


class Group:
    """
        Manages interactions with the 'groups' collection in the database, handling operations
        such as adding, validating, and updating group and user data.
        Attributes:
            id (int): The unique identifier for the group, typically the group's Telegram ID.
            language (str): The group's default language for communication.
    """

    def __init__(self, db: MDB, group_id: int) -> None:
        """
            Initializes a Group object for managing group data in the database.
            Args:
                db (MDB): The database connection.
                group_id (int): Unique identifier for the group (Telegram group ID).
        """
        self._collection = db["groups"]
        self.id = group_id
        self.language: Optional[str] = None

    async def add_to_db(self) -> None:
        """Inserts the group into the database. If the group already exists, clears the user list."""
        try:
            await self._collection.insert_one(
                {"_id": self.id, "users": [], "language": "en"}
            )
        except DuplicateKeyError:
            await self.clear_users()
        except Exception as e:
            logging.error(f"Error adding group {self.id}: {e}")

    async def clear_users(self) -> None:
        """Clears the users list for this group in the database."""
        try:
            await self._collection.update_one(
                {"_id": self.id},
                {"$set": {"users": []}}
            )
        except Exception as e:
            logging.error(f"Error clearing users for group {self.id}: {e}")

    async def validation(self) -> None:
        """Validates the group's existence in the database. If the group does not exist, adds it."""
        try:
            group_data = await self._collection.find_one({"_id": self.id}, {"language": 1})
            self.language = group_data["language"] if group_data else "en"
            if not group_data:
                await self.add_to_db()
        except Exception as e:
            logging.error(f"Error validating group {self.id}: {e}")

    async def delete_from_db(self) -> None:
        """Deletes the group from the database."""
        try:
            await self._collection.delete_one({"_id": self.id})
        except Exception as e:
            logging.error(f"Error deleting group {self.id}: {e}")

    async def update_id(self, new_group_id: int) -> None:
        """
            Updates the group's ID in the database, reflecting a migration to a new chat ID.
            Args:
                new_group_id (int): The new chat ID for the group.
        """
        try:
            group_data = await self._collection.find_one({"_id": self.id})
            if not group_data:
                raise ValueError(f"Group with ID {self.id} does not exist.")

            group_data["_id"] = new_group_id
            await self._collection.insert_one(group_data)
            await self._collection.delete_one({"_id": self.id})

            self.id = new_group_id
            logging.info(f"Group ID successfully migrated from {self.id} to {new_group_id}")
        except Exception as e:
            logging.error(f"Error updating group ID from {self.id} to {new_group_id}: {e}")

    async def change_language(self, language_code: str) -> None:
        """
            Updates the group's preferred language in the database if it has changed.
            Args:
                language_code (str): The new language code.
        """
        if self.language != language_code:
            self.language = language_code
            try:
                await self._collection.update_one(
                    {"_id": self.id},
                    {"$set": {"language": language_code}}
                )
            except Exception as e:
                logging.error(f"Error changing language for group {self.id}: {e}")

    async def add_user(self, user_id: int, can_be_pinged: bool = True) -> None:
        """
            Adds a new user to the group with the specified ping permissions.
            Args:
                user_id (int): The user's Telegram ID.
                can_be_pinged (bool): Indicates if the user can be pinged. Defaults to True.
        """
        try:
            await self._collection.update_one(
                {"_id": self.id, "users.user_id": {"$ne": user_id}},
                {"$push": {"users": {"user_id": user_id, "can_be_pinged": can_be_pinged}}},
                upsert=True
            )
        except Exception as e:
            logging.error(f"Error adding user {user_id} to group {self.id}: {e}")

    async def user_validation(self, user_id: int) -> None:
        """
            Validates if a user exists in the group. If not, adds the user to the group.
            Args:
                user_id (int): The user's Telegram ID.
        """
        try:
            user_exists = await self._collection.find_one(
                {"_id": self.id, "users.user_id": user_id},
                {"users.user_id": 1}
            )
            if not user_exists:
                await self.add_user(user_id)
        except Exception as e:
            logging.error(f"Error validating user {user_id} in group {self.id}: {e}")

    async def delete_user(self, user_id: int) -> None:
        """
        Removes a user from the group.

        Args:
            user_id (int): The user's Telegram ID.
        """
        try:
            await self._collection.update_one(
                {"_id": self.id},
                {"$pull": {"users": {"user_id": user_id}}}
            )
        except Exception as e:
            logging.error(f"Error deleting user {user_id} from group {self.id}: {e}")

    async def bulk_users_insert(self, user_ids: List[int]) -> None:
        """
            Bulk inserts users into the group's users array field.
            Args:
                user_ids (List[int]): A list of user IDs to be added to the group.
        """
        try:
            with suppress(DuplicateKeyError):
                if user_ids:
                    await self._collection.update_one(
                        {"_id": self.id},
                        {"$addToSet": {
                            "users": {"$each": [{"user_id": user_id, "can_be_pinged": True} for user_id in user_ids]}
                        }}
                    )
        except Exception as e:
            logging.error(f"Error during bulk addition of users to group {self.id}: {e}")

    async def update_user_ping_permission(self, user_id: int, allowed_to_be_pinged: bool = True) -> None:
        """
        Updates the pinging permission for a specified user in the group.

        Args:
            user_id (int): The unique Telegram ID of the user.
            allowed_to_be_pinged (bool): Indicates whether the user is allowed to be pinged (default is True).
        """
        try:
            await self._collection.update_one(
                {"_id": self.id, "users.user_id": user_id},
                {"$set": {"users.$.can_be_pinged": allowed_to_be_pinged}}
            )
        except Exception as e:
            logging.error(f"Error updating ping permission for user {user_id} in group {self.id}: {e}")

    async def get_user_ids(self, only_pingable: bool = False, exclude_user_id: int | None = None) -> List[int]:
        """
            Retrieves a list of user IDs in the group, optionally filtered by ping permission.
            Args:
                only_pingable (bool): If True, return only the IDs of users who can be pinged (default is False).
                exclude_user_id (int | None): ID of the user that sent this request and will not be included.
            Returns:
                List[int]: A list of user IDs.
        """
        try:
            all_user_data = await self.get_all_user_data()
            return [
                user["user_id"]
                for user in all_user_data
                if (not only_pingable or user.get("can_be_pinged", False)) and (
                        exclude_user_id is None or user["user_id"] != exclude_user_id)
            ]
        except Exception as e:
            logging.error(f"Error retrieving user IDs for group {self.id}: {e}")
            return []

    async def get_all_user_data(self) -> List[Dict[str, bool]]:
        """
            Retrieves all user records from the group, including their IDs and ping permission status.
            Returns:
                List[Dict[str, Optional[str]]]: A list of dictionaries containing user data.
        """
        try:
            group_data = await self._collection.find_one(
                {"_id": self.id},
                {"users.user_id": 1, "users.can_be_pinged": 1}
            )
            return group_data.get("users", []) if group_data else []
        except Exception as e:
            logging.error(f"Error retrieving all user data for group {self.id}: {e}")
            return []

    async def count_users(self) -> int:
        """
            Counts the number of users in the group.
            Returns:
                int: Number of users in the group.
        """
        try:
            result = await self._collection.aggregate([
                {"$match": {"_id": self.id}},
                {"$project": {"number_of_users": {"$size": "$users"}}}
            ]).to_list(length=1)
            return result[0]["number_of_users"] if result else 0
        except Exception as e:
            logging.error(f"Error counting users in group {self.id}: {e}")
            return 0
