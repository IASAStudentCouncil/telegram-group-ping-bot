from aiogram import F, Router
from aiogram.types import Message

from src.config import admin_chat_id

router = Router(name=__name__)  # Router for admin chat handling


@router.message(F.text == "ping", F.chat.id == admin_chat_id)
async def ping_pong(message: Message) -> None:
    """Hidden command used for health checks to verify the bot's responsiveness. Available only on admin chat."""
    await message.reply("pong")
