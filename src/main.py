import asyncio
import logging

from config import configure_logging
from db import *
from bot import *


async def main() -> None:
    """
        Main asynchronous function to start the bot.

        Establishes connection to MongoDB, configures logging, and starts the bot polling.
    """

    # Initialize logging configuration
    configure_logging()

    # Establish MongoDB connection and configure database
    try:
        client = await connect_to_mongo()
        mdb = await setup_database(client)
        logging.info("MongoDB connection established")
    except Exception as e:
        logging.error("MongoDB failure. Exiting!")
        logging.exception(e)
        return

    # Begin polling to handle updates
    try:
        logging.info("Starting bot polling...")
        await dp.start_polling(bot, db=mdb)
    except Exception as e:
        logging.error("An error occurred while polling!")
        logging.exception(e)
    finally:
        # Close bot session cleanly after polling ends
        await bot.session.close()
        logging.info("Bot session closed!")

if __name__ == '__main__':
    asyncio.run(main())
