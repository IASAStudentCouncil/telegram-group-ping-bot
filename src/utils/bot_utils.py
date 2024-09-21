import logging

from motor.core import AgnosticDatabase as MDB

from src.bot import bot
from src.config import AdminMessages as AM
from src.config import admin_chat_id
from src.config.text import GroupMessages as GM
from src.db import Group, User, get_group_ids_list


async def send_message_to_groups(db: MDB, message_template: dict, action: str) -> None:
    """
        Sends a message to all groups in the database and logs the result.
        Args:
            db (MDB): MongoDB database instance.
            message_template (dict): The message template (e.g., BOT_HAS_BEEN_STARTED or BOT_HAS_BEEN_STOPPED).
            action (str): A string indicating whether it's a startup or shutdown operation.
    """
    group_ids = [id_ for id_ in await get_group_ids_list(db) if id_ != admin_chat_id]
    if group_ids:
        group_count = len(group_ids)
        sended_count = 0
        for _id in group_ids:
            group = Group(db, _id)
            await group.validation()
            try:
                await bot.send_message(_id, message_template[group.language])
                sended_count += 1
            except Exception as e:
                logging.error(f"Failed to send message to group {_id}: {e}")

        admin = User(db, admin_chat_id)
        await admin.validation()
        await bot.send_message(admin_chat_id,
                               AM.BOT_REPORT_MESSAGE[admin.language].format(action, group_count, sended_count))

        logging.info(f"{action} message sent to {f'{sended_count}/{group_count}' if group_count != 0 else 0} groups.")


async def send_bot_startup_message(db: MDB) -> None:
    """Sends the startup message to all groups."""
    await send_message_to_groups(db, GM.BOT_HAS_BEEN_STARTED, "Startup")


async def send_bot_shutdown_message(db: MDB) -> None:
    """Sends the shutdown message to all groups."""
    await send_message_to_groups(db, GM.BOT_HAS_BEEN_STOPPED, "Endup")


async def send_admin_startup_message(db: MDB) -> None:
    """Sends the startup report to the admin chat."""
    admin = User(db, admin_chat_id)
    await admin.validation()
    await bot.send_message(admin_chat_id, AM.BOT_STARTUP_MESSAGE[admin.language])


async def send_admin_shutdown_message(db: MDB) -> None:
    """Sends the shutdown report to the admin chat."""
    admin = User(db, admin_chat_id)
    await admin.validation()
    await bot.send_message(admin_chat_id, AM.BOT_SHUTDOWN_MESSAGE[admin.language])

__all__ = ("send_message_to_groups",
           "send_bot_startup_message",
           "send_bot_shutdown_message",
           "send_admin_startup_message",
           "send_admin_shutdown_message")
