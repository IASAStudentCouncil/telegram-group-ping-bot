from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.config import admin_chat_id

router = Router(name=__name__)  # Router for admin chat handling


@router.message(Command("ping"), F.from_user.id == admin_chat_id)
async def ping_pong(message: Message):
    """Hidden command used for health checks to verify the bot's responsiveness."""
    await message.reply("pong")
