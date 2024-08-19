# Dictionary containing message templates for the bot in different languages

# These messages are used for private chat interactions
private_messages = {
    "start": {
        "en": "Hey! I'm *Ping Bot* 😊\n\n"
              "Type /help to explore all my commands.\n"
              "Or tap the button below to add me to your group chat and start pinging!",
        "uk": "Привіт! Я — *Ping Bot* 😊\n\n"
              "Напишіть /help, щоб ознайомитись з усіма моїми командами.\n"
              "Або натисніть кнопку нижче, щоб додати мене до вашої групи і почати відмічати учасників!"
    },
    "help": {
        "en": "I can help you ping members in your group quickly, like in Discord. "
              "Here are some commands you can use:\n\n"
              "*Personal Chat Commands:*\n"
              "/language - to choose your preferred language.\n"
              "/add_to_group - to add me to a group chat.\n\n"
              "*Group Chat Commands:*\n"
              "****\n\n"
              "Use these commands to enhance your group chat experience!",
        "uk": "Я можу допомогти вам швидко відмічати учасників у вашій групі. "
              "Ось деякі команди, які ви можете використовувати:\n\n"
              "*Персональний чат:*\n"
              "/language - для зміни мови чату.\n"
              "/addtogroup - щоб додати мене до вашої групи.\n\n"
              "*Груповий чат:*\n"
              "****\n\n"
              "Використовуйте ці команди, щоб покращити комунікацію в групових чатах!"
    },
    "choice_language": {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
    },
    "language_selected": {
        "en": "Language selected 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "uk": "Мову обрано 🇺🇦󠁧󠁢󠁥󠁮󠁧󠁿"
    },
    "add_to_group": {
        "en": "Tap the button to add me to your group chat. Let's get pinging!",
        "uk": "Натисніть, щоб додати мене до групи 😌"
    },
    "ignore_commands_in_private": {
        "en": "Command is only available in group chat. Check /help for more information.",
        "uk": "Команда допуступна лише в груповому чаті. Скористайтеся /help аби дізнатися більше."
    }
}

# Dictionary to store text for group messages
group_messages = {
    "start": {
        "en": "Hey! I'm *Ping Bot* 😊\n\n"
              "Type /help to explore all my commands.\n",
        "uk": "Привіт! Я — *Ping Bot* 😊\n\n"
              "Напишіть /help, щоб ознайомитись з усіма моїми командами.\n"
    },
    "help": {
        "en": "I can help you ping members in your group quickly, like in Discord. "
              "Here are commands you can use:\n\n"
              "****\n\n",
        "uk": "Я допоможу вам швидко відмічати учасників у вашій групі. "
              "Ось команди, які ви можете використовувати:\n\n"
              "****\n\n"
    },
    "choice_language": {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
    },
    "language_selected": {
        "en": "Language selected 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "uk": "Мову обрано 🇺🇦󠁧󠁢󠁥󠁮󠁧󠁿"
    },
    "allow_pinging": {
        "en": "Let's get pinging!",
        "uk": "Тепер я можу тебе відмічати!"
    },
    "forbide_pinging": {
        "en": "Ok!",
        "uk": "Добре, більше не буду"
    },
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
