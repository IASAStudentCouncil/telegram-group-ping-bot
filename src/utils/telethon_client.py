from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from typing import List, Dict
import os

from src.config import telegram_api_id, telegram_api_hash


def create_telethon_client() -> TelegramClient:
    """Creates and returns a Telethon TelegramClient instance."""
    session_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        '..', 'system', 'bot_session.session'
    )
    os.makedirs(os.path.dirname(session_file_path), exist_ok=True)
    return TelegramClient(session_file_path, telegram_api_id, telegram_api_hash)


async def parse_group_chat_user_ids(client: TelegramClient,
                                    group_id: int,
                                    only_admins: bool = False) -> List[int]:
    """
        Fetches user IDs from a specified Telegram group, filtering out deleted accounts and bots.
        Optionally retrieves only admin user IDs if `only_admins` is True.
        Args:
            client (TelegramClient): The Telethon client instance used to interact with the Telegram API.
            group_id (int): The unique identifier of the Telegram group.
            only_admins (bool): If True, only admin user IDs are returned. Defaults to False.
        Returns:
            List[int]: A list of user IDs that are not deleted and not bots.
    """
    return [
        user.id async for user in
        client.iter_participants(
            group_id,
            filter=ChannelParticipantsAdmins if only_admins else None
        )
        if not user.deleted and not user.bot
    ]


async def parse_user_data(client: TelegramClient, user_id: int) -> Dict:
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
        'id': user_entity.id,
        'username': user_entity.username,
        'first_name': user_entity.first_name
    }


__all__ = ("TelegramClient", "create_telethon_client",
           "parse_group_chat_user_ids", "parse_user_data")
