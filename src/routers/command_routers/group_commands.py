from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType
from aiogram.enums import ContentType

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.keyboards import *
from src.config import bot_name
from src.config import group_messages as messages
from src.config import available_languages as languages

router = Router(name=__name__)      # Router for group command handling


@router.message(F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def new_group_member(message: Message, db: MDB):
    for chat_member in message.new_chat_members:
        if not chat_member.is_bot:
            user_id = chat_member.id
            username = chat_member.username
            first_name = chat_member.first_name
            user = User(db, user_id, username, first_name)

            await user.user_validation()
        elif chat_member.username == bot_name:
            group_id = message.chat.id
            group = Group(db, group_id)

            await group.add_group_to_db()


@router.message(F.content_type == ContentType.LEFT_CHAT_MEMBER)
async def delete_group_member(message: Message, db: MDB):
    left_member = message.left_chat_member
    if not left_member.is_bot:
        user_id = left_member.id
        username = left_member.username
        first_name = left_member.first_name

        user = User(db, user_id, username, first_name)
        await user.user_validation()
    elif left_member.username == bot_name:
        group_id = message.chat.id
        group = Group(db, group_id)

        await group.delete_group_from_db()
