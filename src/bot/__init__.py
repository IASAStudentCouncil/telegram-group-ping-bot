from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from src.config import bot_token

default_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN,
                                          link_preview_is_disabled=True)    # Default properties with Markdown
bot = Bot(token=bot_token, default=default_properties)                      # Initialize Bot with token and properties

__all__ = ("bot",)
