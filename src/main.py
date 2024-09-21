import asyncio
import logging
import os
from datetime import datetime

from aiogram import Dispatcher

from bot import *
from config import admin_chat_id, bot_token, configure_logging
from db import *
from routers import *
from utils import (
    check_all_groups,
    create_telethon_client,
    send_bot_endup_message,
    send_bot_startup_message,
)


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

    telethon_client = create_telethon_client()
    try:
        await telethon_client.start(bot_token=bot_token)  # await is required
        logging.info("Telethon client started successfully.")
    except Exception as e:
        logging.error("Failed to start Telethon client!")
        logging.exception("Exception details:", exc_info=e)
        return

    try:
        logging.info("Start polling...")
        dp = Dispatcher()
        dp.include_router(router=main_router)

        await check_all_groups(mdb, telethon_client)

        polling_task = dp.start_polling(bot, db=mdb, telethon_client=telethon_client)
        admin_startup_message_task = bot.send_message(
            admin_chat_id,
            f"*Bot started* ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
        )
        startup_message_task = send_bot_startup_message(mdb)
        await asyncio.gather(polling_task, admin_startup_message_task, startup_message_task)
    except Exception as e:
        logging.error("An error occurred while polling!")
        logging.exception("Exception details:", exc_info=e)
        client.close()
    finally:
        await bot.session.close()
        logging.info("Bot session closed!")
        await telethon_client.disconnect()
        logging.info("Telethon client disconnected!")

        await bot.send_message(admin_chat_id, f"*Bot stopped* ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        await send_bot_endup_message(mdb)

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
