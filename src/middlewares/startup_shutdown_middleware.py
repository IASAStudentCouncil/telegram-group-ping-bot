import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.utils import validate_all_groups, send_bot_action_message


class StartupShutdownMiddleware(BaseMiddleware):
    """Middleware to handle bot startup and shutdown actions."""
    def __init__(self, db, tc):
        self.db = db
        self.tc = tc
        super().__init__()

    async def __call__(self, handler, event: TelegramObject, data: dict):
        """
            Middleware call during regular bot operations.
            This does not need to modify the event flow in this case.
        """
        return await handler(event, data)

    async def on_startup(self):
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

    async def on_shutdown(self):
        """This method will be called when the bot is shutting down."""
        logging.info("Bot is shutting down, sending shutdown message...")
        try:
            await send_bot_action_message(self.db, "Shutdown")
        except Exception as e:
            logging.error(f"Failed to send shutdown message: {e}")
