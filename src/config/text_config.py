# Dictionary containing message templates for the bot in different languages

# These messages are used for private chat interactions
private_messages = {
    "start": {
        "en": "Hey! I'm *Ping Bot* 😊\n\n"
              "Type /help to explore all my commands.\n"
              "Or tap the button below to add me to your group chat and start pinging!",
        "uk": "Привіт! Я — *Ping Bot* 😊\n\n"
              "Напишіть /help, щоб ознайомитись з усіма моїми командами.\n"
              "Або натисніть кнопку нижче, щоб додати мене напряму до вашої групи і почати відмічати учасників!"
    },
    "help": {
        "en": "I can help you ping members in your group quickly, like in Discord. "
              "Here are some commands you can use:\n\n"
              "*Personal Chat Commands*\n"
              "/language - to choose your preferred language.\n"
              "/add_to_group - to add me to a group chat.\n\n"
              "*Group Chat Commands*\n"
              "/language - change the group chat language.\n"
              "/pingme - allow yourself to be pinged.\n"
              "/dontpingme - disable pings for yourself.\n"
              "/here - ping only users who allowed it.\n"
              "/everyone - ping all users.\n"
              "/members - get a list of all users in the group, that I know.\n\n"
              "Use these commands to enhance your group chat experience!",
        "uk": "Я можу допомогти вам швидко відмічати учасників у вашій групі. "
              "Ось деякі команди, які ви можете використовувати:\n\n"
              "*Персональний чат*\n"
              "/language - для зміни мови чату.\n"
              "/addtogroup - щоб додати мене до вашої групи.\n\n"
              "*Груповий чат*\n"
              "/pingme - дозволити пінгувати себе.\n"
              "/dontpingme - заборонити пінгувати себе.\n"
              "/here - відмітити лише тих, хто дозволив пінгати себе.\n"
              "/everyone - відмітити всіх учасників.\n"
              "/members - отримати список всіх учасників групи, які мені відомі.\n\n"
              "Використовуйте ці команди, щоб покращити комунікацію в групових чатах!"
    },
    "choice_language": {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
    },
    "language_changed": {
        "en": "Language selected 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "uk": "Мову обрано 🇺🇦󠁧󠁢󠁥󠁮󠁧󠁿"
    },
    "add_to_group": {
        "en": "Tap the button to add me to your group chat. Let's get pinging!",
        "uk": "Натисніть, щоб додати мене до вашої групи 😌"
    },
    "ignore_group_commands_in_private": {
        "en": "Command is only available in group chat. Check /help",
        "uk": "Команда допуступна лише в груповому чаті. Скористайтеся /help"
    }
}

# Dictionary to store text for group messages
group_messages = {
    "start": {
        "en": "Hey! I'm *Ping Bot* 😊\n\n"
              "Type /help to explore all my commands.",
        "uk": "Привіт! Я — *Ping Bot* 😊\n\n"
              "Використовуйте /help, щоб ознайомитись з усіма моїми командами."
    },
    "help": {
        "en": "I can help you ping members in your group quickly, like in Discord. "
              "Here are some commands you can use:\n\n"
              "/language - change the group chat language.\n"
              "/pingme - allow yourself to be pinged.\n"
              "/dontpingme - disable pings for yourself.\n"
              "/here - ping only users who allowed it.\n"
              "/everyone - ping all users.\n"
              "/members - get a list of all users in the group, that I know.",
        "uk": "Я допоможу вам швидко відмічати учасників у вашій групі. "
              "Ось команди, які ви можете використовувати:\n\n"
              "/language - змінити мову групового чату.\n"
              "/pingme - дозволити пінгувати себе.\n"
              "/dontpingme - заборонити пінгувати себе.\n"
              "/here - відмітити тільки тих, хто дозволив пінгувати себе.\n"
              "/everyone - відмітити абсолютно всіх учасників.\n"
              "/members - список всіх учасників групи, які мені відомі."
    },
    "add_user": {
        "en": "Welcome to the group! I'm *Ping Bot* 😊\n"
              "Type /help to learn how to use me.",
        "uk": "Ласкаво просимо до групи! Я — *Ping Bot* 😊\n"
              "Напишіть /help, щоб дізнатися, як користуватись мною."
    },
    "delete_user": {
        "en": "Goodbye! 😣",
        "uk": "Прощавайте! 😣"
    },
    "choice_language": {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
    },
    "language_changed": {
        "en": "Language selected 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "uk": "Мову обрано 🇺🇦󠁧󠁢󠁥󠁮󠁧󠁿"
    },
    "allow_pinging": {
        "en": "Let's get pinging 😉",
        "uk": "Тепер я зможу пінгувати вас 😉"
    },
    "forbide_pinging": {
        "en": "Ok. I will not ping you 🥲",
        "uk": "Добре, домовились 🥲"
    },
    "get_all_pingable_users": {
        "en": "*Able to be pinged:*",
        "uk": "*Користувачі, яких я можу пінгувати:*"
    },
    "get_all_unpingable_users": {
        "en": "*Disable to ping them:*",
        "uk": "*Користувачі, які не дозволили пінгувати себе:*"
    },
    "no_pingable_users": {
        "en": "*No one has allowed pinging.*",
        "uk": "*Не знайдено жодного користувача, який дозволив пунгувати себе.*"
    },
    "how_to_ping_pinable_users": {
        "en": "Type /here to ping only users who allow it.",
        "uk": "Скористайтеся /here, щоб відмітити всіх, хто дозволив пінгувати себе."
    },
    "add_to_list_users_info": {
        "en": "If anyone is not on the list, they just need to use any of my commands, and I'll them.",
        "uk": "Якщо когось немає у списку, вони можуть використати будь-яку з моїх команд, і я додам їх до своєї бази."
    },
    "only_you_in_group_chat": {
        "en": "*It seems like you're the only one I know in this group right now.*\n\n"
              "To use /here or /everyone, I need to be familiar with at least one other person. "
              "I can only recognize users who have interacted with me or those who have just joined the group. "
              "Use /members to see the list of everyone I know in this group.",
        "uk": "*Здається, що наразі я знаю лише вас у цій групі.*\n\n"
              "Щоб використати /here або /everyone, мені потрібно знати хоча б ще одну людину. "
              "Я можу розпізнавати тільки тих користувачів, "
              "які взаємодіяли зі мною, або тих, хто щойно приєднався до групи. "
              "Використовуйте /members, щоб побачити список усіх, кого я знаю в цій групі."
    },
    "no_one_allow_pinging": {
        "en": "*No one currently allows pinging.*\n\n"
              "To change this, use /pingme to enable pinging for yourself. "
              "You can also check /members to see who has allowed or disabled pinging.",
        "uk": "*Ніхто наразі не дозволив пінгування.*\n\n"
              "Щоб це змінити, скористайтеся /pingme, щоб дозволити пінгування для себе. "
              "Також можете переглянути /members, щоб побачити, хто дозволив або заборонив пінгування."
    }
}

# For texts associated with reply keyboard markup buttons
keyboards_text = {

}

# For texts associated with inline keyboard buttons
inline_keyboards_text = {
    "add_to_group_button": {
        "en": "Add to group chat",
        "uk": "Додати до групи"
    }
}
