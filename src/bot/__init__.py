from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from src.routers import *
from src.config import bot_token

default_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)    # Default properties with Markdown
bot = Bot(token=bot_token, default=default_properties)                      # Initialize Bot with token and properties
dp = Dispatcher()                                                           # Create a Dispatcher for managing updates
dp.include_router(router=main_router)                                       # Register main router for handling commands

__all__ = ("bot", "dp")
