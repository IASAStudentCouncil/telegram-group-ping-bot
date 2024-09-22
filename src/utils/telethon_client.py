import logging
import os

from motor.core import AgnosticDatabase as MDB
from telethon import TelegramClient, errors

from src.config import admin_chat_id, telegram_api_hash, telegram_api_id
from src.db import Group, get_group_ids_list


def create_telethon_client() -> TelegramClient:
    """Creates and returns a Telethon TelegramClient instance."""
    session_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "..", "system", "bot_session.session"
    )
    os.makedirs(os.path.dirname(session_file_path), exist_ok=True)
    return TelegramClient(session_file_path, telegram_api_id, telegram_api_hash)


async def parse_group_chat_user_ids(
    client: TelegramClient,
    group_id: int,
    exclude_user_id: int | None = None,
    include_bot_id: int | None = None
) -> list[int]:
    """
        Fetches user IDs from a specified Telegram group, filtering out deleted accounts. Optionally includes a specific bot.

        Args:
            client (TelegramClient): The Telethon client instance used to interact with the Telegram API.
            group_id (int): The unique identifier of the Telegram group.
            exclude_user_id (int | None): ID of the user that sent this request and will be excluded. Default is None.
            include_bot_id (int | None): ID of a specific bot to include in the results, if provided. Default is None.

        Returns:
            list[int]: A list of user IDs that are not deleted, optionally including a specific bot.
    """
    return [
        user.id async for user in client.iter_participants(group_id)
        if not user.deleted
        and (user.bot and user.id == include_bot_id or not user.bot)
        and (exclude_user_id is None or user.id != exclude_user_id)
    ]


async def parse_user_data(client: TelegramClient, user_id: int) -> dict:
    """
        Fetches and returns a dictionary containing the user's ID, username, and first name
        from Telegram using the provided user ID.
        Args:
            client (TelegramClient): The Telethon client instance used to interact with the Telegram API.
            user_id (int): The unique identifier of the Telegram user.
        Returns:
            dict: A dictionary containing the user's ID, username, and first name.
        """
    user_entity = await client.get_entity(user_id)
    return {
        "id": user_entity.id,
        "username": user_entity.username,
        "first_name": user_entity.first_name
    }


async def check_group_status(db: MDB, client: TelegramClient, group_id: int) -> None:
    """
        This function:
        - Checks if the group has been migrated to a supergroup and updates the ID if necessary.
        - Fetches participants from the group and compares them to the database records.
        - Removes users from the database who are no longer in the group.
        - Deletes the group from the database if the bot is no longer a participant.
        Args:
            db (MDB): The MongoDB instance used for group management.
            client (TelegramClient): The Telethon client instance used to interact with the Telegram API.
            group_id (int): The unique identifier of the Telegram group.
    """
    group = Group(db, group_id)
    try:
        chat = await client.get_entity(group_id)
        if hasattr(chat, "migrated_to") and chat.migrated_to is not None:
            new_id = chat.migrated_to.channel_id
            await group.update_id(new_id)

        bot_id = (await client.get_me()).id
        participants_ids = await parse_group_chat_user_ids(client, group_id, include_bot_id=bot_id)

        bot_is_in_group = bot_id in participants_ids

        if not bot_is_in_group:
            await group.delete_from_db()
        else:
            db_user_ids = await group.get_user_ids()

            for db_user_id in db_user_ids:
                if db_user_id not in participants_ids:
                    await group.delete_user(db_user_id)

            for user_id in participants_ids:
                if user_id not in db_user_ids and user_id != bot_id:
                    await group.add_user(user_id)

    except (errors.UserKickedError, errors.UserNotParticipantError, errors.ChatIdInvalidError):
        logging.info(f"Group {group_id} no longer exists. Deleting record.")
        await group.delete_from_db()
    except errors.FloodWaitError as e:
        logging.error(f"Too many requests. Waiting {e.seconds} seconds before retrying.")
    except Exception as e:
        logging.error(f"Unexpected error when checking group {group_id}: {e}")


async def validate_all_groups(db: MDB, client: TelegramClient) -> None:
    """
        Iterates through all Telegram group IDs stored in the database and checks their status.
        Args:
            db (MDB): The MongoDB instance used for group management.
            client (TelegramClient): The Telethon client instance used to interact with the Telegram API.
    """
    group_ids = [id_ for id_ in await get_group_ids_list(db) if id_ != admin_chat_id]
    for _id in group_ids:
        await check_group_status(db, client, _id)


__all__ = ("TelegramClient", "create_telethon_client",
           "parse_group_chat_user_ids", "parse_user_data", "validate_all_groups")
