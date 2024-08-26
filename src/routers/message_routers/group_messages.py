from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMember
from aiogram.enums.chat_type import ChatType
from aiogram.enums import ContentType
from aiogram.utils import markdown

from motor.core import AgnosticDatabase as MDB

from src.db import *
from src.keyboards import *
from src.config import bot_name
from src.config import group_messages as messages
from src.utils import TelegramClient, parse_user_ids, parse_user_data

router = Router(name=__name__)      # Router for group event handling


@router.message(
    F.content_type.in_(
        [ContentType.NEW_CHAT_MEMBERS,
         ContentType.GROUP_CHAT_CREATED,
         ContentType.SUPERGROUP_CHAT_CREATED]
    ),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP])
)
async def new_group_and_member(message: Message, db: MDB, telethon_client: TelegramClient) -> None:
    """
        Handles new chat creation and members joining group.
        If the new member is the bot itself, it sends a welcome message.
        If the new member is a user, it adds them to the group in the database.
    """
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.validation()

    if message.group_chat_created or message.supergroup_chat_created:
        await group.add_to_db()
        await message.answer(text=messages["parsing_users"][group.language])
        user_ids = await parse_user_ids(telethon_client, group.id)
        await group.bulk_users_insert(user_ids)
        await message.answer(text=messages["start"][group.language])
    else:
        for chat_member in message.new_chat_members:
            if chat_member.is_bot and chat_member.username == bot_name:
                await group.add_to_db()
                await message.answer(text=messages["parsing_users"][group.language])
                user_ids = await parse_user_ids(telethon_client, group.id)
                await group.bulk_users_insert(user_ids)
                await message.answer(text=messages["start"][group.language])
            else:
                user_id = chat_member.id
                await group.user_validation(user_id)
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
            await group.clear_users()
    else:
        user_id = left_member.id
        await group.delete_user(user_id)
        try:
            await message.reply(text=messages["delete_user"][group.language])
        except Exception as e:
            await message.answer(text=messages["delete_user"][group.language])


@router.message(F.content_type == ContentType.MIGRATE_TO_CHAT_ID,
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def chat_id_migration(message: Message, db: MDB) -> None:
    """
        Handles the migration of a group's chat ID when a group is upgraded to a supergroup.
        It updates the group ID in the database to reflect the new chat ID.
    """
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.validation()

    new_group_id = message.migrate_to_chat_id
    if new_group_id:
        await group.update_id(new_group_id)


@router.message(
    F.from_user.is_bot,
    Command(
        commands=['start', 'help', 'language', 'pingme',
                  'dontpingme', 'here', 'everyone', 'members']
    )
)
async def ignore_commands_from_other_bot():
    """
        Ignores commands issued by other bots.
        This function is triggered when a message is sent by another bot
        containing any of the specified commands
    """
    pass


async def setup_group(db: MDB, message: Message) -> Group:
    """
        Initializes and validates the Group and User objects within a MongoDB collection.
        Args:
            db (MDB): The MongoDB database connection.
            message (Message): The incoming Telegram message.
        Returns:
            Group: The validated Group object.
    """
    group_id = message.chat.id
    user_id = message.from_user.id

    group = Group(db, group_id)
    await group.validation()
    await group.user_validation(user_id)

    return group


@router.message(Command(commands=["start", "help"]),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def start_help(message: Message, db: MDB) -> None:
    """
        Handles '/start' and '/help' commands in group chats.
        Sends a welcome message if the command is '/start', otherwise sends a help message.
    """
    group = await setup_group(db, message)
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
    group = await setup_group(db, message)
    await message.answer(text=messages["choice_language"][group.language],
                         reply_markup=build_language_markup())


@router.message(Command("pingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def allow_to_ping_user(message: Message, db: MDB) -> None:
    """
        Handles the '/pingme' command in group chats.
        Allows the user to be pinged in the group.
    """
    group = await setup_group(db, message)
    await group.update_user_ping_permission(message.from_user.id, allowed_to_be_pinged=True)
    await message.reply(text=messages["allow_pinging"][group.language])


@router.message(Command("dontpingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def do_not_ping_user(message: Message, db: MDB) -> None:
    """
        Handles the '/dontpingme' command in group chats.
        Disables pinging for the user in the group.
    """
    group = await setup_group(db, message)
    await group.update_user_ping_permission(message.from_user.id, allowed_to_be_pinged=False)
    await message.reply(text=messages["forbide_pinging"][group.language])


@router.message(Command("here"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_pingable_users(message: Message, db: MDB) -> None:
    """
        Handles the '/here' command in group chats.
        Pings all users in the group who have allowed themselves to be pinged.
    """
    group = await setup_group(db, message)
    user_ids = await group.get_user_ids(only_pingable=True)

    if user_ids:
        user_ids = [user_id for user_id in user_ids if user_id != message.from_user.id]
        if user_ids:
            message_text = markdown.link(f"@here", f"https://t.me/{bot_name}")
            for user_id in user_ids:
                message_text += markdown.link(f"‎", f"tg://user?id={user_id}")
        else:
            message_text = messages["only_you_in_group_chat"][group.language]
    else:
        message_text = messages["no_one_allow_pinging"][group.language]

    await message.reply(text=message_text)


@router.message(Command("everyone"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_everyone(message: Message, db: MDB) -> None:
    """
        Handles the '/everyone' command in group chats.
        Pings all users in the group, except the user who issued the command.
    """
    group = await setup_group(db, message)
    user_ids = await group.get_user_ids()
    user_ids = [user_id for user_id in user_ids if user_id != message.from_user.id]
    if user_ids:
        message_text = markdown.link(f"@еvеryone", f"https://t.me/{bot_name}")
        for user_id in user_ids:
            message_text += markdown.link(f"‎", f"tg://user?id={user_id}")
    else:
        message_text = messages["only_you_in_group_chat"][group.language]

    await message.reply(text=message_text)


@router.message(Command("members"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def show_users_list(message: Message, db: MDB, telethon_client: TelegramClient) -> None:
    """
        Handles the '/members' command in group chats.
        Sends a list of all users in the group, separating those who allow pinging and those who don't.
    """
    group = await setup_group(db, message)
    users_data_list = await group.get_all_user_data()
    users_list = [
        {
            **await parse_user_data(telethon_client, user_data["user_id"]),
            "can_be_pinged": user_data["can_be_pinged"]
        }
        for user_data in users_data_list
    ]

    pingable_users = [
        f"*{i + 1}.* {user['first_name']} (`{user['username']}`)"
        for i, user in enumerate(users_list) if user["can_be_pinged"]
    ]
    unpingable_users = [
        f"*{i + 1}.* {user['first_name']} (`{user['username']}`)"
        for i, user in enumerate(users_list) if not user["can_be_pinged"]
    ]
    pingable_users_text = '\n'.join(pingable_users)
    unpingable_users_text = '\n'.join(unpingable_users)

    pingable_users_text = (f"{messages['get_all_pingable_users'][group.language]}\n"
                           f"{pingable_users_text}\n\n") if pingable_users else ""
    unpingable_users_text = (f"{messages['get_all_unpingable_users'][group.language]}\n"
                             f"{unpingable_users_text}\n\n") if unpingable_users else ""

    if pingable_users_text:
        message_text = (f"{pingable_users_text}{unpingable_users_text}"
                        f"{messages['how_to_ping_pinable_users'][group.language]} "
                        f"{messages['add_to_list_users_info'][group.language]}")
    else:
        message_text = (f"{messages['no_pingable_users'][group.language]}\n\n"
                        f"{unpingable_users_text}"
                        f"{messages['add_to_list_users_info'][group.language]}")
    await message.answer(text=message_text)
