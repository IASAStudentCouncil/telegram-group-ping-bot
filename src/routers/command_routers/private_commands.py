from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.keyboards import *
from src.config import private_messages as messages

router = Router(name=__name__)      # Router for private command handling


@router.message(Command(commands=['start', 'help']), F.chat.type == ChatType.PRIVATE)
async def start_help(message: Message, db: MDB) -> None:
    """
        Handles '/start' and '/help' commands in private chats. Clears any previous state, validates user,
        and responds with the appropriate message and keyboard based on the command.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    user_chat_language = message.from_user.language_code

    user = User(db, user_id, username, first_name, user_chat_language)
    await user.validation()

    if "/start" in message.text:
        await message.answer(text=messages["start"][user.language],
                             reply_markup=build_add_to_group_markup(user.language))
    else:
        await message.answer(text=messages["help"][user.language])


async def setup_user(db: MDB, message: Message) -> User:
    """
        Helper function to initialize and validate a User object.
        Args:
            db (MDB): The MongoDB database connection.
            message (Message): The incoming Telegram message containing user information.
        Returns:
            User: User objects.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    user = User(db, user_id, username, first_name)
    await user.validation()

    return user


@router.message(Command('addtogroup'), F.chat.type == ChatType.PRIVATE)
async def add_to_group(message: Message, db: MDB) -> None:
    """Handles the '/addtogroup' command which allows users to add the bot to a group chat."""
    user = await setup_user(db, message)
    await message.answer(text=messages["add_to_group"][user.language],
                         reply_markup=build_add_to_group_markup(user.language))


@router.message(Command('language'), F.chat.type == ChatType.PRIVATE)
async def change_language(message: Message, db: MDB) -> None:
    """Initiates language change process by presenting a language selection keyboard."""
    user = await setup_user(db, message)
    await message.answer(text=messages["choice_language"][user.language],
                         reply_markup=build_language_markup())


@router.message(Command(commands=['pingme', 'dontpingme', 'here', 'everyone', 'members']),
                F.chat.type == ChatType.PRIVATE)
async def ignore_group_commands(message: Message, db: MDB) -> None:
    """Handles commands that are meant for group chats but are mistakenly sent in private messages."""
    user = await setup_user(db, message)
    await message.reply(text=messages["ignore_group_commands_in_private"][user.language])
