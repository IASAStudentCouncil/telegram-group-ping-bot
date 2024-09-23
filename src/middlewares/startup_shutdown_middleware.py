import logging
from typing import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from motor.core import AgnosticDatabase as MDB
from telethon import TelegramClient

from src.utils import send_bot_action_message, validate_all_groups


class StartupShutdownMiddleware(BaseMiddleware):
    """Middleware to handle bot startup and shutdown actions."""
    def __init__(self, db: MDB, tc: TelegramClient) -> None:
        super().__init__()
        self.db = db
        self.tc = tc

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict], Awaitable],
            event: TelegramObject,
            data: dict
    ) -> TelegramObject:
        """
            Middleware call during regular bot operations.
            This does not need to modify the event flow in this case.
        """
        return await handler(event, data)

    async def on_startup(self) -> None:
        """This method will be called when the bot starts."""
        logging.info("Bot is starting, starting group validation and sending startup message...")
        try:
            await validate_all_groups(self.db, self.tc)
        except Exception as e:
            logging.error(f"Failed to validate groups: {e}")
        try:
            await send_bot_action_message(self.db, "Startup")
        except Exception as e:
            logging.error(f"Failed to send startup message: {e}")

    async def on_shutdown(self) -> None:
        """This method will be called when the bot is shutting down."""
        logging.info("Bot is shutting down, sending shutdown message...")
        try:
            await send_bot_action_message(self.db, "Shutdown")
        except Exception as e:
            logging.error(f"Failed to send shutdown message: {e}")
