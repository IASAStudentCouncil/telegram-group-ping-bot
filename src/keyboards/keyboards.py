from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.config import keyboards_text as text
from src.config import available_languages


def build_language_markup() -> ReplyKeyboardMarkup:
    """
    This keyboard presents buttons for each available language, configured to disappear after one use and to fit the screen size.

    Returns:
        ReplyKeyboardMarkup: A reply keyboard with language selection buttons.

    """
    builder = ReplyKeyboardBuilder()
    for languages in available_languages.values():
        builder.add(KeyboardButton(text=languages))

    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )


__all__ = ('build_language_markup',)
