# These messages are used for private chat interactions
class PrivateMessages:
    START = {
        "en": "Hey! I'm *Ping Bot* 😊",
        "uk": "Привіт! Я — *Ping Bot* 😊"
    }
    HELP = {
        "en": (
            "I can help you quickly ping members in your group, just like in Discord. "
            "Here are some commands you can use:\n\n"
            "*Personal Chat Commands*\n"
            "/language - Choose your preferred language.\n\n"
            "*Group Chat Commands*\n"
            "/language - Change the group chat language.\n"
            "/pingme - Allow yourself to be pinged.\n"
            "/dontpingme - Disable pings for yourself.\n"
            "/here - Ping only users who have allowed it.\n"
            "/everyone - Ping all users.\n"
            "/admins - Ping all administrators.\n"
            "/getmembers - Get a list of all users in the group that I know.\n"
            "/getadmins - Get a list of all administrators.\n\n"
            "Use these commands to enhance your group chat experience!"
        ),
        "uk": (
            "Я можу допомогти вам швидко відмічати учасників у вашій групі. "
            "Ось деякі команди, які ви можете використовувати:\n\n"
            "*Персональний Чат Команди*\n"
            "/language - Оберіть бажану мову.\n\n"
            "*Команди для Групового Чату*\n"
            "/language - Змініть мову групового чату.\n"
            "/pingme - Дозвольте пінгувати себе.\n"
            "/dontpingme - Забороніть пінгувати себе.\n"
            "/here - Відмітити лише тих, хто дозволив пінгувати себе.\n"
            "/everyone - Відмітити всіх учасників.\n"
            "/admins - Відмітити всіх адміністраторів.\n"
            "/getmembers - Отримати список всіх учасників групи, які мені відомі.\n"
            "/getadmins - Отримати список всіх адміністраторів.\n\n"
            "Використовуйте ці команди, щоб покращити комунікацію в груповому чаті!"
        )
    }
    CHOICE_LANGUUAGE = {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
    }
    LANGUAGE_CHANGED = {
        "en": "Language selected 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "uk": "Мову обрано 🇺🇦󠁧󠁢󠁥󠁮󠁧󠁿"
    }
    IGNORE_GROUP_COMMANDS_IN_PRIVATE_CHAT = {
        "en": "Command is only available in group chat. Check /help",
        "uk": "Команда допуступна лише в груповому чаті. Скористайтеся /help"
    }
