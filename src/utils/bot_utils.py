import logging

from motor.core import AgnosticDatabase as MDB

from src.bot import bot
from src.config import admin_chat_id
from src.config.text import GroupMessages as GM
from src.db import Group, get_group_ids_list


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
        admin_message = (f"📊 *Bot {action} Report*\n\n"
                         f"- *Total Active Groups:* {group_count} \n"
                         f"- *{action} Message Sent:* "
                         f"{f'{sended_count}/{group_count}' if group_count != 0 else 0} groups")
        await bot.send_message(admin_chat_id, admin_message)
        logging.info(f"{action} message sent to {f'{sended_count}/{group_count}' if group_count != 0 else 0} groups.")


async def send_bot_startup_message(db: MDB) -> None:
    """Sends the startup message to all groups."""
    await send_message_to_groups(db, GM.BOT_HAS_BEEN_STARTED, "Startup")


async def send_bot_endup_message(db: MDB) -> None:
    """Sends the shutdown message to all groups."""
    await send_message_to_groups(db, GM.BOT_HAS_BEEN_STOPPED, "Endup")

__all__ = ("send_message_to_groups", "send_bot_startup_message", "send_bot_endup_message")
