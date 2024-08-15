from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from src.routers import *
from src.config import bot_token

# Define default properties with Markdown support for message formatting
default_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)

# Initialize Bot with specified token and default properties
bot = Bot(token=bot_token, default=default_properties)

# Create a Dispatcher for managing updates
dp = Dispatcher()

# Integrate main router for handling commands
dp.include_router(router=main_router)

__all__ = ("bot", "dp")
