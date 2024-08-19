from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums.chat_type import ChatType

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.config import private_messages as messages
from src.config import available_languages as languages

router = Router(name=__name__)      # Router for private callbacks handling


@router.callback_query(F.data.in_(languages.keys()),
                       F.message.chat.type == ChatType.PRIVATE)
async def set_language(call: CallbackQuery, db: MDB) -> None:
    """Sets the user's language based on their selection and confirms the update."""

    user_id = call.from_user.id
    username = call.from_user.username
    language = call.data

    user = User(db, user_id, username)
    await user.user_validation()
    await user.change_user_language(language)

    await call.message.edit_text(text=messages["language_selected"][language])
