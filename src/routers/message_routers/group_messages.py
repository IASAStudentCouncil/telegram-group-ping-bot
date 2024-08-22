from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.chat_type import ChatType
from aiogram.enums import ContentType
from aiogram.utils import markdown

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.keyboards import *
from src.config import bot_name
from src.config import group_messages as messages

router = Router(name=__name__)      # Router for group event handling


@router.message(
    F.content_type.in_(
        [ContentType.NEW_CHAT_MEMBERS,
         ContentType.GROUP_CHAT_CREATED,
         ContentType.SUPERGROUP_CHAT_CREATED]
    ),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP])
)
async def new_group_and_member(message: Message, db: MDB) -> None:
    """
        Handles new chat creation and members joining group.
        If the new member is the bot itself, it sends a welcome message.
        If the new member is a user, it adds them to the group in the database.
    """
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.validation()
    if message.group_chat_created or message.supergroup_chat_created:
        await message.answer(text=messages["start"][group.language])
    else:
        for chat_member in message.new_chat_members:
            if chat_member.is_bot:
                if chat_member.username == bot_name:
                    await message.answer(text=messages["start"][group.language])
            else:
                user_id = chat_member.id
                username = chat_member.username
                first_name = chat_member.first_name
                user = User(db, user_id, username, first_name)
                await user.validation()
                await group.add_user(user_id)
                await message.reply(text=messages["add_user"][group.language])


@router.message(F.content_type == ContentType.LEFT_CHAT_MEMBER,
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def delete_group_member(message: Message, db: MDB) -> None:
    """
        Handles members leaving the chat. If a user leaves, they are removed from the group in the database.
        If the bot leaves, the group is deleted from the database.
    """
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.validation()
    left_member = message.left_chat_member

    if left_member.is_bot:
        if left_member.username == bot_name:
            await group.delete_from_db()
    else:
        user_id = left_member.id
        username = left_member.username
        first_name = left_member.first_name
        user = User(db, user_id, username, first_name)
        await user.validation()
        await group.delete_user(user_id)
        try:
            await message.reply(text=messages["delete_user"][group.language])
        except Exception as e:
            pass


@router.message(
    F.from_user.is_bot,
    Command(
        commands=['start', 'help', 'language', 'pingme',
                  'dontpingme', 'here', 'everyone', 'members']
    )
)
async def ignore_commands_from_other_bot(message: Message):
    """
        Ignores commands issued by other bots.
        This function is triggered when a message is sent by another bot
        containing any of the specified commands
    """
    pass


async def setup_group_and_user(db: MDB, message: Message) -> (Group, User):
    """
        Helper function to initialize and validate Group and User objects.
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

    user = User(db, user_id, username, first_name)
    await user.validation()

    group = Group(db, group_id)
    await group.validation()
    await group.user_validation(user_id)

    return group, user


@router.message(Command(commands=["start", "help"]),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def start_help(message: Message, db: MDB) -> None:
    """
        Handles '/start' and '/help' commands in group chats.
        Sends a welcome message if the command is '/start', otherwise sends a help message.
    """
    group, user = await setup_group_and_user(db, message)
    if "/start" in message.text:
        await message.answer(text=messages["start"][group.language])
    else:
        await message.answer(text=messages["help"][group.language])


@router.message(Command("language"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def change_languge(message: Message, db: MDB) -> None:
    """
        Handles the '/language' command in group chats.
        Sends a language selection keyboard to the chat.
    """
    group, user = await setup_group_and_user(db, message)
    await message.answer(text=messages["choice_language"][group.language],
                         reply_markup=build_language_markup())


@router.message(Command("pingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def allow_to_ping_user(message: Message, db: MDB) -> None:
    """
        Handles the '/pingme' command in group chats.
        Allows the user to be pinged in the group.
    """
    group, user = await setup_group_and_user(db, message)
    await group.update_user_ping_permission(user.id, allowed_to_be_pinged=True)
    await message.reply(text=messages["allow_pinging"][group.language])


@router.message(Command("dontpingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def do_not_ping_user(message: Message, db: MDB) -> None:
    """
        Handles the '/dontpingme' command in group chats.
        Disables pinging for the user in the group.
    """
    group, user = await setup_group_and_user(db, message)
    await group.update_user_ping_permission(user.id, allowed_to_be_pinged=False)
    await message.reply(text=messages["forbide_pinging"][group.language])


@router.message(Command("here"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_pingable_users(message: Message, db: MDB) -> None:
    """
        Handles the '/here' command in group chats.
        Pings all users in the group who have allowed themselves to be pinged.
    """
    group, user = await setup_group_and_user(db, message)
    message_text = markdown.link(f"@here", f"https://t.me/{bot_name}")
    user_list = await group.get_user_ids(only_pingable=True)
    for user_id in user_list:
        if user_id != message.from_user.id:
            message_text += markdown.link(f"‎", f"tg://user?id={user_id}")
    await message.answer(text=message_text, disable_web_page_preview=True)


@router.message(Command("everyone"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_everyone(message: Message, db: MDB) -> None:
    """
        Handles the '/everyone' command in group chats.
        Pings all users in the group, except the user who issued the command.
    """
    group, user = await setup_group_and_user(db, message)
    message_text = markdown.link(f"@еvеryone", f"https://t.me/{bot_name}")
    user_list = await group.get_user_ids()
    for user_id in user_list:
        if user_id != message.from_user.id:
            message_text += markdown.link(f"‎", f"tg://user?id={user_id}")
    await message.answer(text=message_text, disable_web_page_preview=True)


@router.message(Command("members"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def show_users_list(message: Message, db: MDB) -> None:
    """
        Handles the '/members' command in group chats.
        Sends a list of all users in the group, separating those who allow pinging and those who don't.
    """
    group, user = await setup_group_and_user(db, message)

    pingable_users, unpingable_users = "", ""
    i, j = 1, 1
    users_list = await group.get_all_user_data()
    for users in users_list:
        id_, username, first_name, can_be_pinged = users
        if can_be_pinged:
            pingable_users += f"*{i}.* {first_name} (`{username}`)\n"
            i += 1
        else:
            unpingable_users += f"*{j}.* {first_name} (`{username}`)\n"
            j += 1
    pingable_users = (f"{messages['get_all_pingable_users'][group.language]}\n"
                      f"{pingable_users}\n") if pingable_users else ""
    unpingable_users = (f"{messages['get_all_unpingable_users'][group.language]}\n"
                        f"{unpingable_users}\n") if unpingable_users else ""

    if pingable_users:
        message_text = (f"{pingable_users}{unpingable_users}"
                        f"{messages['how_to_ping_pinable_users'][group.language]} "
                        f"{messages['add_to_list_users_info'][group.language]}")
    else:
        message_text = (f"{messages['no_pingable_users'][group.language]}\n\n"
                        f"{unpingable_users}"
                        f"{messages['add_to_list_users_info'][group.language]}")
    await message.answer(text=message_text)
