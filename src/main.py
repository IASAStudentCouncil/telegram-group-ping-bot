import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import *
from db import *
from routers import *


async def main() -> None:
    # Configure logging
    configure_logging()

    # Connect to MongoDB
    try:
        mdb = await ping_mongo_db()
        logging.info("MongoDB connection established.")
    except Exception as e:
        logging.error("MongoDB failure. Exiting.")
        logging.exception(e)
        return

    # Create Bot and Dispatcher instances
    default_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    bot = Bot(token=bot_token, default=default_properties)
    dp = Dispatcher()

    # Register routers
    dp.include_router(router=main_router)
    logging.info("Connected all routers to dispatcher successfully.")

    # Start polling
    try:
        logging.info("Starting bot polling...")
        await dp.start_polling(bot, db=mdb)
    except Exception as e:
        logging.error("An error occurred while polling.")
        logging.exception(e)
    finally:
        await bot.session.close()
        logging.info("Bot session closed.")

if __name__ == '__main__':
    asyncio.run(main())
