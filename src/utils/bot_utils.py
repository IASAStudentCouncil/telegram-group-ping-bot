import logging

from motor.core import AgnosticDatabase as MDB

from src.bot import bot
from src.config import AdminMessages as AM
from src.config import GroupMessages as GM
from src.config import admin_chat_id
from src.db import Group, User, get_group_ids_list


async def send_message_to_groups(db: MDB, message_template: dict, action: str, admin_language: str) -> None:
    """
        Sends a message to all groups in the database and logs the result.
        Args:
            db (MDB): MongoDB database instance.
            message_template (dict): The message template (e.g., BOT_HAS_BEEN_STARTED or BOT_HAS_BEEN_STOPPED).
            action (str): A string indicating whether it's a startup or shutdown operation.
            admin_language (str): The language to use for the admin's report message.
    """
    group_ids = [id_ for id_ in await get_group_ids_list(db) if id_ != admin_chat_id]
    if group_ids:
        group_count = len(group_ids)
        sended_count = 0

        for group_id in group_ids:
            group = Group(db, group_id)
            await group.validation()
            try:
                await bot.send_message(group_id, message_template[group.language])
                sended_count += 1
            except Exception as e:
                logging.error(f"Failed to send message to group {group_id}: {e}")

        try:
            await bot.send_message(admin_chat_id,
                                   AM.BOT_REPORT_MESSAGE[admin_language].format(action, group_count, sended_count))
        except Exception as e:
            logging.error(f"Failed to send report to admin: {e}")

        logging.info(f"{action} message sent to {sended_count}/{group_count} groups.")


async def send_bot_action_message(db: MDB, action: str) -> None:
    """
        Sends both the admin and group messages based on the action (startup or shutdown).
        Args:
            db (MDB): MongoDB database instance.
            action (str): Either "Startup" or "Endup" to specify the action.
    """
    ACTION_MESSAGES = {
        "Startup": [GM.BOT_HAS_BEEN_STARTED, AM.BOT_STARTUP_ADMIN_MESSAGE],
        "Shutdown": [GM.BOT_HAS_BEEN_STOPPED, AM.BOT_SHUTDOWN_ADMIN_MESSAGE]
    }

    try:
        admin = User(db, admin_chat_id)
    except Exception:
        admin = Group(db, admin_chat_id)
    await admin.validation()
    admin_language = admin.language

    try:
        await bot.send_message(admin_chat_id, ACTION_MESSAGES[action][1][admin.language])
    except Exception as e:
        logging.error(f"Failed to send {action} message to admin: {e}")

    try:
        await send_message_to_groups(db, ACTION_MESSAGES[action][0], action, admin_language)
    except Exception as e:
        logging.error(f"Failed to send {action} message to groups: {e}")


__all__ = ("send_message_to_groups", "send_bot_action_message")
