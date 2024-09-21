import asyncio
import logging
import os

from aiogram import Dispatcher

from bot import *
from config import bot_token, configure_logging
from db import *
from routers import *
from utils import *


async def main() -> None:
    """
        Main asynchronous function to start the bot.
        Establishes connection to MongoDB, configures logging, and starts the bot polling.
    """
    if not os.path.exists("system"):  # creates 'system' folder were .log and .session files will be. REQUIRED!!!
        os.makedirs("system")
    configure_logging()

    try:
        client = await connect_to_mongo()
        mdb = await setup_database(client)
        logging.info("MongoDB connection established")
    except Exception as e:
        logging.error("MongoDB failure. Exiting!")
        logging.exception("Exception details:", exc_info=e)
        return

    tc = create_telethon_client()
    try:
        await tc.start(bot_token=bot_token)  # await is required
        logging.info("Telethon client started successfully.")
    except Exception as e:
        logging.error("Failed to start Telethon client!")
        logging.exception("Exception details:", exc_info=e)
        return

    try:
        logging.info("Start polling...")
        dp = Dispatcher()
        dp.include_router(router=main_router)

        await check_all_groups(mdb, tc)

        await asyncio.gather(
            dp.start_polling(bot, db=mdb, telethon_client=tc),
            send_admin_startup_message(mdb),
            send_bot_startup_message(mdb))
    except Exception as e:
        logging.error("An error occurred while polling!")
        logging.exception("Exception details:", exc_info=e)
        client.close()
    finally:
        await bot.session.close()
        logging.info("Bot session closed!")
        await tc.disconnect()
        logging.info("Telethon client disconnected!")

        await send_admin_shutdown_message(mdb)
        await send_bot_shutdown_message(mdb)

        client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot was stopped by the user (KeyboardInterrupt). Exiting...")
    except Exception as e:
        logging.error("An unexpected error occurred during bot execution")
        logging.exception("Exception details:", exc_info=e)
    finally:
        logging.info("Bot shutdown process completed!")
