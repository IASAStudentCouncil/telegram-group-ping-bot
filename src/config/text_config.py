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
              "*Personal Chat Commands:*\n"
              "/language - to choose your preferred language.\n"
              "/add_to_group - to add me to a group chat.\n\n"
              "*Group Chat Commands:*\n"
              "/language - change the group chat language.\n"
              "/pingme - allow yourself to be pinged.\n"
              "/dontpingme - disable pings for yourself.\n"
              "/here - ping only users who allowed it.\n"
              "/everyone - ping all users.\n"
              "/members - get a list of all users in the group, that I know.\n\n"
              "Use these commands to enhance your group chat experience!",
        "uk": "Я можу допомогти вам швидко відмічати учасників у вашій групі. "
              "Ось деякі команди, які ви можете використовувати:\n\n"
              "*Персональний чат:*\n"
              "/language - для зміни мови чату.\n"
              "/addtogroup - щоб додати мене до вашої групи.\n\n"
              "*Груповий чат:*\n"
              "/pingme - дозволити пінгати себе.\n"
              "/dontpingme - заборонити пінгати себе.\n"
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
        "uk": "Натисніть, щоб додати мене до групи 😌"
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
              "Використуйте /help, щоб ознайомитись з усіма моїми командами."
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
              "/pingme - дозволити пінгати себе.\n"
              "/dontpingme - заборонити пінгати себе.\n"
              "/here - відмітити тільки тих, хто дозволив пінгати.\n"
              "/everyone - відмітити всіх учасників.\n"
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
        "uk": "Тепер я зможу відмічати вас 😉"
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
    "how_to_ping_pinable_users": {
        "en": "Type /here to ping only users who allow it.",
        "uk": "Скористайтеся /here, щоб відмітити всіх, хто дозволив пінгувати себе."
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
