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


@router.message(F.content_type == ContentType.NEW_CHAT_MEMBERS,
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def new_group_member(message: Message, db: MDB) -> None:
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.get_group_language()
    for chat_member in message.new_chat_members:
        if not chat_member.is_bot:
            user_id = chat_member.id
            username = chat_member.username
            first_name = chat_member.first_name
            user = User(db, user_id, username, first_name)
            await user.user_validation()
            await group.add_user(user_id)
        elif chat_member.username == bot_name:
            await message.answer(text=messages["start"][group.language])


@router.message(F.content_type == ContentType.LEFT_CHAT_MEMBER,
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def delete_group_member(message: Message, db: MDB) -> None:
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.get_group_language()
    left_member = message.left_chat_member
    if not left_member.is_bot:
        user_id = left_member.id
        username = left_member.username
        first_name = left_member.first_name
        user = User(db, user_id, username, first_name)
        await user.user_validation()
        await group.delete_user(user_id)
    elif left_member.username == bot_name:
        await group.delete_group_from_db()


async def setup_group_and_user(db: MDB, message: Message) -> (Group, User):
    """
    Helper function to initialize Group and User objects.

    Args:
        db (MDB): The MongoDB database connection.
        message (Message): The incoming Telegram message.

    Returns:
        tuple: A tuple containing the Group and User objects.
    """
    group_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    group = Group(db, group_id)
    user = User(db, user_id, username, first_name)
    await user.user_validation()
    await group.get_group_language()
    await group.user_validation(user_id)

    return group, user


@router.message(Command(commands=["start", "help"]),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def start_help(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)
    if "/start" in message.text:
        await message.answer(text=messages["start"][group.language])
    else:
        await message.answer(text=messages["help"][group.language])


@router.message(Command("language"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def change_languge(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)
    await message.answer(text=messages["choice_language"][group.language])


@router.message(Command("pingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def allow_to_ping_user(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)
    await group.allow_to_ping_user(user.id)
    await message.answer(text=messages["allow_pinging"][group.language])


@router.message(Command("dontpingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def do_not_ping_user(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)
    await group.forbid_user_pinging(user.id)
    await message.answer(text=messages["forbide_pinging"][group.language])


@router.message(Command("here"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_pingable_users(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)

    message_text = ""
    usernames_list = await group.get_pingable_usernames()
    for usernames in usernames_list:
        message_text += f"@{usernames} "
    await message.answer(text=message_text)


@router.message(Command("everyone"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_everyone(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)

    message_text = ""
    usernames_list = await group.get_all_usernames()
    for usernames in usernames_list:
        message_text += f"@{usernames} "
    await message.answer(text=message_text)


@router.message(Command("getusers"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def show_users_list(message: Message, db: MDB) -> None:
    group, user = await setup_group_and_user(db, message)

    message_text = ""
    users_list = await group.get_all_user_data()
    for i, users in enumerate(users_list):
        is_allowed_to_be_pinged = "can be pinged." if users[2] else "cannot be pinged."
        message_text += f"{i+1}. {users[0]} ({users[1]}), {is_allowed_to_be_pinged}\n"
    await message.answer(text=message_text)
