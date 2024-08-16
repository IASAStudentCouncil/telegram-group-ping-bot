from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import inline_keyboards_text as text
from src.config import available_languages


def build_language_markup() -> InlineKeyboardMarkup:
    """
        Creates an inline keyboard with buttons for selecting the user's preferred language.
        Returns:
            InlineKeyboardMarkup: An inline keyboard with language selection buttons.
    """

    builder = InlineKeyboardBuilder()
    for language_code, language in available_languages.items():
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
    builder.button(text=text["add_to_group_button"][language], url="https://t.me/group_mate_tag_bot?startgroup=test")
    return builder.as_markup()


__all__ = ("build_language_markup", "build_add_to_group_markup")
