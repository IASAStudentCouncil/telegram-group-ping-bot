from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from motor.core import AgnosticDatabase as MDB

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message, db: MDB):
    await message.answer(
        text="Hi, I'm Mate Tag Bot."  # Заглушка
    )
