import logging

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

from src.config import mongo_uri
from .schema_validators import *


async def ping_mongo_db(uri: str = mongo_uri) -> MDB:
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

    db_name = 'telegram-group-tag'
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
