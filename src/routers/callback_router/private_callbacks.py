from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.types import CallbackQuery
from motor.core import AgnosticDatabase as MDB

from src.config import AVAILABLE_LANGUAGES as languages
from src.config import PrivateMessages as PM
from src.db import *
from src.keyboards import *

router = Router(name=__name__)      # Router for private callbacks handling


@router.callback_query(F.data == "commands_list",
                       F.message.chat.type == ChatType.PRIVATE)
async def start_help(call: CallbackQuery, db: MDB) -> None:
    """Handle scenario when user click on 'My commands' via start message."""
    user_id = call.from_user.id
    user = User(db, user_id)
    await user.validation()
    await call.message.edit_text(text=PM.HELP[user.language],
                                 reply_markup=build_add_to_group_markup(user.language))


@router.callback_query(F.data.in_(languages.keys()),
                       F.message.chat.type == ChatType.PRIVATE)
async def change_user_language(call: CallbackQuery, db: MDB) -> None:
    """Sets the user's language based on their selection and confirms the update."""
    user_id = call.from_user.id
    language = call.data

    user = User(db, user_id)
    await user.validation()
    await user.change_language(language)

    await call.message.edit_text(text=PM.LANGUAGE_CHANGED[language])
