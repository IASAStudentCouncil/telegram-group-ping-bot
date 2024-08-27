from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums.chat_type import ChatType

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.config import GroupMessages as GM
from src.config import available_languages as languages

router = Router(name=__name__)  # Router for group callbacks handling


@router.callback_query(F.data.in_(languages.keys()),
                       F.message.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def change_user_language(call: CallbackQuery, db: MDB) -> None:
    """Sets the group's language based on language selection and confirms the update."""
    group_id = call.message.chat.id
    user_id = call.from_user.id
    language_code = call.data

    group = Group(db, group_id)
    await group.validation()
    await group.user_validation(user_id)
    await group.change_language(language_code)
    await call.message.edit_text(text=GM.LANGUAGE_CHANGED[language_code])
