from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.chat_type import ChatType

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.keyboards import *
from src.config import private_messages as messages
from src.config import available_languages as languages

# Initialize router for private command handling
router = Router(name=__name__)


@router.message(Command(commands=['start', 'help']), F.chat.type == ChatType.PRIVATE)
async def start(message: Message, db: MDB):
    """
    Handles '/start' and '/help' commands in private chats. Clears any previous state, validates user,
    and responds with the appropriate message and keyboard based on the command.
    """

    user_id = message.from_user.id
    username = message.from_user.username
    user_chat_language = message.from_user.language_code

    user = User(db, user_id, username, user_chat_language)
    await user.user_validation()
    if "/start" in message.text:
        await message.answer(text=messages["start"][user.language],
                             reply_markup=build_add_to_group_markup(user.language))
    else:
        await message.answer(text=messages["help"][user.language],
                             reply_markup=ReplyKeyboardRemove())


@router.message(Command('addtogroup'), F.chat.type == ChatType.PRIVATE)
async def add_to_group(message: Message, db: MDB):
    """
    Handles the '/addtogroup' command which allows users to add the bot to a group chat.
    """

    user_id = message.from_user.id
    username = message.from_user.username

    user = User(db, user_id, username)
    await user.user_validation()

    await message.answer(text=messages["add_to_group"][user.language],
                         reply_markup=build_add_to_group_markup(user.language))


@router.message(Command('language'), F.chat.type == ChatType.PRIVATE)
async def change_language(message: Message, db: MDB):
    """
    Initiates language change process by presenting a language selection keyboard.
    """
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(db, user_id, username)
    await user.user_validation()

    await message.answer(text=messages["choice_language"][user.language],
                         reply_markup=build_language_markup())


@router.message(F.text.in_(languages.values()),
                F.chat.type == ChatType.PRIVATE)
async def set_language(message: Message, db: MDB):
    """
    Sets the user's language based on their selection and confirms the update.
    """

    user_id = message.from_user.id
    username = message.from_user.username

    user = User(db, user_id, username)
    await user.user_validation()

    language = list(languages.keys())[list(languages.values()).index(message.text)]
    await user.change_language(language)

    await message.reply(text=messages["language_selected"][user.language],
                        reply_markup=ReplyKeyboardRemove())
