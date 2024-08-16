from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import inline_keyboards_text as text


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


__all__ = ("build_add_to_group_markup",)
