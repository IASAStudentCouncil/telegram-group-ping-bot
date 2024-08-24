from telethon import TelegramClient
from telethon.sessions import StringSession
from typing import List, Dict
import os

from src.config import telegram_api_id, telegram_api_hash


def create_telethon_client():
    """Creates and returns a Telethon TelegramClient instance."""
    return TelegramClient("bot", telegram_api_id, telegram_api_hash)


async def parse_users(client: TelegramClient, group_id: int) -> List[Dict]:
    """
        Fetches all active users from a specified Telegram group using a Telethon client.
        Args:
            client (TelegramClient): The Telethon client instance used to interact with the Telegram API.
            group_id (int): The unique identifier of the Telegram group.
        Returns:
            List[Dict]: A list of dictionaries, each containing details of an active user (non-deleted and non-bot) in the group.
                        Each dictionary includes the user's id, username, and first name.
    """
    users = []

    async for user in client.iter_participants(group_id):
        if not user.deleted and not user.bot:
            user_details = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name
            }
            users.append(user_details)

    return users

__all__ = ("TelegramClient", "create_telethon_client", "parse_users")
