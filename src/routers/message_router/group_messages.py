from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.enums.chat_type import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import markdown
from motor.core import AgnosticDatabase as MDB
from telethon import TelegramClient

from src.bot import bot
from src.config import GROUP_LIMIT_SIZE, MENTION_PER_MESSAGE_LIMIT, bot_name
from src.config import GroupMessages as GM
from src.db import *
from src.keyboards import *
from src.utils import parse_group_chat_user_ids, parse_user_data

router = Router(name=__name__)      # Router for group event handling


async def new_group_validation(group: Group, message: Message, telethon_client: TelegramClient) -> None:
    """Fetch new group and parse all users"""
    await group.add_to_db()
    await message.answer(text=GM.PARSING_USERS[group.language])
    user_ids = await parse_group_chat_user_ids(telethon_client, group.id)
    await group.bulk_users_insert(user_ids)
    if await group.count_users() > GROUP_LIMIT_SIZE:
        await message.answer(text=GM.GROUP_HAS_MORE_THAN_500_USERS[group.language])
    else:
        await message.answer(text=GM.USERS_HAS_BEEN_PARSED[group.language])


@router.message(
    F.content_type.in_(
        [ContentType.NEW_CHAT_MEMBERS,
         ContentType.GROUP_CHAT_CREATED,
         ContentType.SUPERGROUP_CHAT_CREATED]
    ),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP])
)
async def new_member_validation(message: Message, db: MDB, telethon_client: TelegramClient) -> None:
    """
        Handles new chat creation and members joining group.
        If the new member is the bot itself, it fetchs group and all users, add sends a welcome message.
        If the new member is a user, it adds them to the group in the database.
    """
    group_id = message.chat.id
    group = Group(db, group_id)
    await group.validation()

    if message.group_chat_created or message.supergroup_chat_created:
        await new_group_validation(group, message, telethon_client)
    else:
        for chat_member in message.new_chat_members:
            if chat_member.is_bot and chat_member.username == bot_name:
                await new_group_validation(group, message, telethon_client)
            else:
                user_id = chat_member.id
                await group.user_validation(user_id)
                if await group.count_users() == GROUP_LIMIT_SIZE + 1:
                    await message.answer(text=GM.GROUP_HIT_SIZE_LIMIT[group.language])


@router.message(F.content_type == ContentType.LEFT_CHAT_MEMBER,
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def group_member_deleting(message: Message, db: MDB) -> None:
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
        await group.delete_user(user_id)
        if await group.count_users() <= GROUP_LIMIT_SIZE:
            await message.answer(text=GM.GROUP_UNHIT_SIZE_LIMIT[group.language])


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
        commands=["start", "help", "language", "pingme",
                  "dontpingme", "here", "everyone", "getmembers",
                  "admins", "getadmins", "chatid"]
    ),
    F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP])
)
async def ignore_commands_from_other_bot() -> None:
    """
        Just in case if it's ever happened. :)

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
async def start_and_help(message: Message, db: MDB) -> None:
    """
        Handles '/start' and '/help' commands in group chats.
        Sends a welcome message if the command is '/start', otherwise sends a help message.
    """
    group = await setup_group(db, message)
    if "/start" in message.text:
        await message.answer(text=GM.START[group.language])
    else:
        if await group.count_users() > GROUP_LIMIT_SIZE:
            await message.answer(text=GM.RESTRICTED_HELP[group.language])
        else:
            await message.answer(text=GM.HELP[group.language])


@router.message(Command("language"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def choice_new_languge(message: Message, db: MDB) -> None:
    """
        Handles the '/language' command in group chats.
        Sends a language selection keyboard to the chat.
    """
    group = await setup_group(db, message)
    member = await bot.get_chat_member(group.id, message.from_user.id)
    if member.status not in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
        await message.reply(text=GM.ONLY_ADMINS_OR_OWNER_CAN_CHANGE_LANGUAGE[group.language])
    else:
        await message.reply(text=GM.CHOICE_LANGUAGE[group.language],
                             reply_markup=build_language_markup())


@router.message(Command("pingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def allow_to_ping_user(message: Message, db: MDB) -> None:
    """
        Handles the '/pingme' command in group chats.
        Allows the user to be pinged in the group.
    """
    group = await setup_group(db, message)
    if await group.count_users() > GROUP_LIMIT_SIZE:
        await message.reply(text=GM.COMMAND_IS_BEEN_RESTRICTED[group.language])
    else:
        await group.update_user_ping_permission(message.from_user.id, allowed_to_be_pinged=True)
        await message.reply(text=GM.ALLOW_USER_PINGING[group.language])


@router.message(Command("dontpingme"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def forbide_to_ping_user(message: Message, db: MDB) -> None:
    """
        Handles the '/dontpingme' command in group chats.
        Disables pinging for the user in the group.
    """
    group = await setup_group(db, message)
    if await group.count_users() > GROUP_LIMIT_SIZE:
        await message.reply(text=GM.COMMAND_IS_BEEN_RESTRICTED[group.language])
    else:
        await group.update_user_ping_permission(message.from_user.id, allowed_to_be_pinged=False)
        await message.reply(text=GM.FORBIDE_USER_PINGING[group.language])


@router.message(Command("here"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_only_pingable_users(message: Message, db: MDB) -> None:
    """
        Handles the '/here' command in group chats.
        Pings all users in the group who have allowed themselves to be pinged.
        Due to limitation of 50 mention per message it offen send multiple messages with mentions.
    """
    group = await setup_group(db, message)
    if await group.count_users() > GROUP_LIMIT_SIZE:
        await message.reply(text=GM.COMMAND_IS_BEEN_RESTRICTED[group.language])
    else:
        user_ids = await group.get_user_ids(only_pingable=True)
        if not user_ids:
            await message.reply(GM.NO_ONE_ALLOW_PINGING[group.language])
        else:
            user_ids = [user_id for user_id in user_ids if user_id != message.from_user.id]
            if not user_ids:
                await message.reply(GM.ONLY_ONE_USER_IN_GROUP[group.language])
            else:
                message_base = markdown.link("@here", f"https://t.me/{bot_name}")
                user_count = len(user_ids)
                users_mentioned = 0
                for i in range(0, user_count, MENTION_PER_MESSAGE_LIMIT):
                    users_batch = user_ids[i:i + MENTION_PER_MESSAGE_LIMIT]
                    users_mentioned += len(users_batch)
                    message_text = message_base + "".join(
                        markdown.link("‎", f"tg://user?id={user_id}") for user_id in users_batch
                    )
                    if user_count > MENTION_PER_MESSAGE_LIMIT:
                        message_text += f" ({users_mentioned}/{user_count})"
                    if i == 0:
                        await message.reply(text=message_text)
                    else:
                        await message.answer(text=message_text)


@router.message(Command("everyone"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_everyone_in_group(message: Message, db: MDB) -> None:
    """
        Handles the '/everyone' command in group chats.
        Pings all users in the group, except the user who issued the command.
        Due to limitation of 50 mention per message it offen send multiple messages with mentions.
    """
    group = await setup_group(db, message)
    if await group.count_users() > GROUP_LIMIT_SIZE:
        await message.reply(text=GM.COMMAND_IS_BEEN_RESTRICTED[group.language])
    else:
        user_id = message.from_user.id
        member = await bot.get_chat_member(group.id, user_id)
        if member.status not in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
            await message.answer(text=GM.ONLY_ADMINS_CAN_USE_THIS_COMMAND[group.language])
        else:
            user_ids = await group.get_user_ids(exclude_user_id=user_id)
            if not user_ids:
                await message.reply(text=GM.ONLY_ONE_USER_IN_GROUP[group.language])
            else:
                message_base = markdown.link("@еvеryone", f"https://t.me/{bot_name}")
                user_count = len(user_ids)
                users_mentioned = 0
                for i in range(0, user_count, MENTION_PER_MESSAGE_LIMIT):
                    users_batch = user_ids[i:i + MENTION_PER_MESSAGE_LIMIT]
                    users_mentioned += len(users_batch)
                    message_text = message_base + "".join(
                        markdown.link("‎", f"tg://user?id={user_id}") for user_id in users_batch
                    )
                    if user_count > MENTION_PER_MESSAGE_LIMIT:
                        message_text += f" ({users_mentioned}/{user_count})"
                    if i == 0:
                        await message.reply(text=message_text)
                    else:
                        await message.answer(text=message_text)


@router.message(Command("getmembers"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def show_members_list(message: Message, db: MDB, telethon_client: TelegramClient) -> None:
    """
        Handles the '/getmembers' command in group chats.
        Sends a list of all users in the group, separating those who allow pinging and those who don't.
    """
    group = await setup_group(db, message)
    if await group.count_users() > GROUP_LIMIT_SIZE:
        message_text = GM.COMMAND_IS_BEEN_RESTRICTED[group.language]
    else:
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
        pingable_users_text = "\n".join(pingable_users)
        unpingable_users_text = "\n".join(unpingable_users)

        pingable_users_text = (f"{GM.GET_ALL_PINGABLE_USERS_LIST_TITLE[group.language]}\n"
                               f"{pingable_users_text}\n\n") if pingable_users else ""
        unpingable_users_text = (f"{GM.GET_ALL_UNPINGABLE_USERS_LIST_TITLE[group.language]}\n"
                                 f"{unpingable_users_text}\n\n") if unpingable_users else ""

        if pingable_users_text:
            message_text = (f"{pingable_users_text}{unpingable_users_text}"
                            f"{GM.HOW_TO_PING_PINDABLE_USERS[group.language]} "
                            f"{GM.HOW_TO_ADD_USERS_TO_THE_LIST[group.language]}")
        else:
            message_text = (f"{GM.NO_PINGABLE_USERS[group.language]}\n\n"
                            f"{unpingable_users_text}"
                            f"{GM.HOW_TO_ADD_USERS_TO_THE_LIST[group.language]}")
    await message.reply(text=message_text)


@router.message(Command("admins"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def ping_admins(message: Message, db: MDB, telethon_client: TelegramClient) -> None:
    """
        Handles the '/admins' command in group chats. Pings all admins in the group.
        Due to limitation of only 50 admins per group chat and 50 mentions per message it only sends one message.
    """
    user_id = message.from_user.id
    group = await setup_group(db, message)
    member = await bot.get_chat_member(group.id, user_id)
    if member.status not in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
        await message.answer(text=GM.ONLY_ADMINS_CAN_USE_THIS_COMMAND[group.language])
    else:
        user_ids = await parse_group_chat_user_ids(telethon_client, group.id)
        admins_ids = [
            user_id for user_id in user_ids
            if (await bot.get_chat_member(group.id, user_id)).status in [ChatMemberStatus.CREATOR,
                                                                         ChatMemberStatus.ADMINISTRATOR]
        ]
        if not admins_ids:
            await message.reply(text=GM.NO_ADMINS_FOUND[group.language])
        elif admins_ids == [user_id]:
            await message.reply(text=GM.THERE_IS_NO_ADMINS_EXCEPT_YOU[group.language])
        else:
            message_base = markdown.link("@admins", f"https://t.me/{bot_name}")
            message_text = message_base + "".join(
                markdown.link("‎", f"tg://user?id={user_id}") for user_id in admins_ids
            )
            await message.reply(text=message_text)


@router.message(Command("getadmins"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def show_admins_list(message: Message, db: MDB, telethon_client: TelegramClient) -> None:
    """
        Handles the '/getadmins' command in group chats.
        Sends a list of all admins (including owner) in the group chat.
    """
    group = await setup_group(db, message)
    user_ids = await parse_group_chat_user_ids(telethon_client, group.id)

    admins_data_list = [
        await parse_user_data(telethon_client, user_id)
        for user_id in user_ids
        if (await bot.get_chat_member(group.id, user_id)).status in [ChatMemberStatus.CREATOR,
                                                                     ChatMemberStatus.ADMINISTRATOR]
    ]

    admins_list = [
        f"*{i + 1}.* {user['first_name']} (`{user['username']}`)"
        for i, user in enumerate(admins_data_list)
    ]
    admins_list_text = "\n".join(admins_list)
    message_text = (f"{GM.GET_ALL_ADMINS_LIST_TITLE[group.language]}\n"
                    f"{admins_list_text}\n\n"
                    f"{GM.HOW_TO_PING_ADMINS[group.language]}")

    await message.reply(text=message_text)


@router.message(Command("chatid"),
                F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def get_chat_id(message: Message) -> None:
    """Send chat id to the chat"""
    await message.reply(text=f"`{message.chat.id}`")
