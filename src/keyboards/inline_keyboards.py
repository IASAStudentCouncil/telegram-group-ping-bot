from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import AVAILABLE_LANGUAGES, bot_name
from src.config import KeyboardButtonsText as KBT


def build_start_markup(language: str) -> InlineKeyboardMarkup:
    """
        Creates an inline keyboard with a button that apears with start message.
        Args:
            language (str): The language key to fetch appropriate button text.
        Returns:
            InlineKeyboardMarkup: The constructed inline keyboard.
        The button directs users to a URL for adding the bot to their Telegram group.
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=KBT.COMMANDS_LIST_BUTTON_TEXT[language],
                                     callback_data="commands_list"))
    builder.add(InlineKeyboardButton(text=KBT.ADD_TO_GROUP_BUTTON_TEXT[language],
                                     url=f"https://t.me/{bot_name}?startgroup=test"))
    return builder.as_markup()


def build_language_markup() -> InlineKeyboardMarkup:
    """
        Creates an inline keyboard with buttons for selecting the user's preferred language.
        Returns:
            InlineKeyboardMarkup: An inline keyboard with language selection buttons.
    """
    builder = InlineKeyboardBuilder()
    for language_code, language in AVAILABLE_LANGUAGES.items():
        builder.add(
            InlineKeyboardButton(
                text=language,
                callback_data=language_code
            )
        )
    builder.adjust(2)
    return builder.as_markup(one_time_keyboard=True)


def build_add_to_group_markup(language: str) -> InlineKeyboardMarkup:
    """
        Creates an inline keyboard with a button that allows adding the bot to a group.
        Args:
            language (str): The language key to fetch appropriate button text.
        Returns:
            InlineKeyboardMarkup: The constructed inline keyboard with a single button.
        The button directs users to a URL for adding the bot to their Telegram group.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text=KBT.ADD_TO_GROUP_BUTTON_TEXT[language],
                   url=f"https://t.me/{bot_name}?startgroup=test")
    return builder.as_markup()


__all__ = ("build_start_markup", "build_language_markup", "build_add_to_group_markup")
