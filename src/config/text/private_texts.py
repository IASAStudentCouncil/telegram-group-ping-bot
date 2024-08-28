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
            "/language - choose your preferred language.\n\n"
            "*Group Chat Commands*\n"
            "/language - change the group chat language.\n"
            "/pingme - allow yourself to be pinged.\n"
            "/dontpingme - disable pings for yourself.\n"
            "/here - ping only users who have allowed it.\n"
            "/everyone - ping all users.\n"
            "/admins - ping all administrators.\n"
            "/getmembers - get a list of all users in the group that I know.\n"
            "/getadmins - get a list of all administrators.\n\n"
            "Use these commands to enhance your group chat experience!"
        ),
        "uk": (
            "Я можу допомогти вам швидко відмічати учасників у вашій групі. "
            "Ось деякі команди, які ви можете використовувати:\n\n"
            "*Персональний Чат Команди*\n"
            "/language - оберіть бажану мову.\n\n"
            "*Команди для Групового Чату*\n"
            "/language - змініть мову групового чату.\n"
            "/pingme - дозвольте пінгувати себе.\n"
            "/dontpingme - забороніть пінгувати себе.\n"
            "/here - відмітити лише тих, хто дозволив пінгувати себе.\n"
            "/everyone - відмітити всіх учасників.\n"
            "/admins - відмітити всіх адміністраторів.\n"
            "/getmembers - отримати список всіх учасників групи, які мені відомі.\n"
            "/getadmins - отримати список всіх адміністраторів.\n\n"
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
