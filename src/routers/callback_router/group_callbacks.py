from aiogram import F, Router
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.enums.chat_type import ChatType
from aiogram.types import CallbackQuery
from motor.core import AgnosticDatabase as MDB

from src.bot import bot
from src.config import AVAILABLE_LANGUAGES as languages
from src.config import GroupMessages as GM
from src.db import *

router = Router(name=__name__)  # Router for group callbacks handling


@router.callback_query(F.data.in_(languages.keys()),
                       F.message.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def change_group_language(call: CallbackQuery, db: MDB) -> None:
    """Sets the group's language based on language selection and confirms the update."""
    user_id = call.from_user.id
    language_code = call.data

    group_id = call.message.chat.id
    group = Group(db, group_id)

    member = await bot.get_chat_member(group_id, user_id)
    if member.status not in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
        await call.message.answer(text=GM.ONLY_ADMINS_OR_OWNER_CAN_CHANGE_LANGUAGE[group.language],
                                  show_alert=True)
    else:
        await group.validation()
        await group.user_validation(user_id)
        await group.change_language(language_code)
        await call.message.edit_text(text=GM.LANGUAGE_CHANGED[language_code])
