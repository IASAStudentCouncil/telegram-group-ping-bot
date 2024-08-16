from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.keyboards import *
from src.config import group_messages as messages
from src.config import available_languages as languages

router = Router(name=__name__)      # Router for group command handling
