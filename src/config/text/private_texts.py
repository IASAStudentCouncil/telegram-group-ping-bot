class PrivateMessages:
    """These messages are used for private chat interactions."""

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
            "/language - change the language settings.\n"
            "/pingme - opt-in to be mentioned with pings.\n"
            "/dontpingme - opt-out of being mentioned.\n"
            "/here - ping all users who have allowed pings.\n"
            "/everyone - ping everyone in the group.\n"
            "/admins - ping all administrators.\n"
            "/getmembers - view a list of all members and their ping preferences.\n"
            "/getadmins - get a list of all administrators.\n\n"
            "Use these commands to enhance your group chat experience!"
        ),
        "uk": (
            "Я можу допомогти вам швидко відмічати учасників у вашій групі. "
            "Ось деякі команди, які ви можете використовувати:\n\n"
            "*Персональний Чат Команди*\n"
            "/language - оберіть бажану мову.\n\n"
            "*Команди для Групового Чату*\n"
            "/language - змініть мовні налаштування.\n"
            "/pingme - дозвольте пінгувати себе.\n"
            "/dontpingme - забороніть пінгувати себе.\n"
            "/here - відмітити лише тих, хто дозволив пінгувати себе.\n"
            "/everyone - відмітити абсолютно всіх учасників групи.\n"
            "/admins - відмітити всіх адміністраторів.\n"
            "/getmembers - отримати список всіх учасників групи з інформацією хто дозволив себе пінгувати.\n"
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
