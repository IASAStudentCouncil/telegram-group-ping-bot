# Store text for group chat messages
class GroupMessages:
    START = {
        "en": ("Hey! I'm *Ping Bot* 😊\n\n"
               "Type /help to explore all my commands."),
        "uk": ("Привіт! Я — *Ping Bot* 😊\n\n"
               "Використовуйте /help, щоб ознайомитись з усіма моїми командами.")
    }
    HELP = {
        "en": (
            "I can help you quickly ping members in your group, similar to Discord. "
            "Here are some commands you can use:\n\n"
            "*Regular Commands:*\n"
            "/pingme - allow yourself to be pinged.\n"
            "/dontpingme - disable pings for yourself.\n"
            "/here - ping only users who have allowed it.\n"
            "/getmembers - get a list of all users in the group chat.\n"
            "/getadmins - get a list of all admins.\n\n"
            "*Admin Commands:*\n"
            "/language - change the group chat language.\n"
            "/everyone - ping all users.\n"
            "/admins - ping all admins.\n"
        ),
        "uk": (
            "Я допоможу вам швидко пінгувати учасників у вашій групі. "
            "Ось команди, які ви можете використовувати:\n\n"
            "*Звичайні команди:*\n"
            "/pingme - дозволити пінгувати себе.\n"
            "/dontpingme - заборонити пінгувати себе.\n"
            "/here - пінганути тільки тих, хто дозволив пінгувати себе.\n"
            "/getmembers - отримати список всіх учасників групи.\n"
            "/getadmins - отримати список всіх адміністраторів.\n\n"
            "*Команди для адміністраторів:*\n"
            "/language - змінити мову групового чату.\n"
            "/everyone - відмітити абсолютно всіх учасників.\n"
            "/admins - відмітити всіх адміністраторів.\n"
        )
    }
    PARSING_USERS = {
        "en": "Wait... Adding all users to my database...",
        "uk": "Зачекайте... Додаю усіх користувачів до бази даних..."
    }
    USERS_HAS_BEEN_PARSED = {
        "en": ("Successfully added all users to my database. Let's get started! "
               "I'm *Ping Bot* 😊. Type /help to explore all my commands."),
        "uk": ("Успішно додав усіх користувачів до моєї бази даних. "
               "Будемо знайомі! Я — *Ping Bot* 😊. "
               "Використовуйте /help, щоб ознайомитись з усіма моїми командами.")
    }
    ADD_USER = {
        "en": ("Welcome to the group! I'm *Ping Bot* 😊\n"
               "Type /help to learn how to use me."),
        "uk": ("Ласкаво просимо до групи! Я — *Ping Bot* 😊\n"
               "Напишіть /help, щоб дізнатися, як користуватись мною.")
    }
    DELETE_USER = {
        "en": "Goodbye! 😣",
        "uk": "Прощавайте! 😣"
    }
    CHOICE_LANGUAGE = {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
    }
    ONLY_ADMINS_OR_OWNER_CAN_CHANGE_LANGUAGE = {
        "en": "Only admins or owner of the group chat can change group language.",
        "uk": "Лише власник та адміни групи мають право змінювати мову."
    }
    LANGUAGE_CHANGED = {
        "en": "Language selected 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "uk": "Мову обрано 🇺🇦󠁧󠁢󠁥󠁮󠁧󠁿"
    }
    ALLOW_USER_PINGING = {
        "en": "Let's get pinging 😉",
        "uk": "Тепер я зможу пінгувати вас 😉"
    }
    FORBIDE_USER_PINGING = {
        "en": "Ok. I will not ping you 🥲",
        "uk": "Добре, домовились 🥲"
    }
    GET_ALL_PINGABLE_USERS_LIST_TITLE = {
        "en": "*Able to be pinged:*",
        "uk": "*Користувачі, яких я можу пінгувати:*"
    }
    GET_ALL_UNPINGABLE_USERS_LIST_TITLE = {
        "en": "*Disable to ping them:*",
        "uk": "*Користувачі, які не дозволили пінгувати себе:*"
    }
    NO_PINGABLE_USERS = {
        "en": "*No one has allowed pinging.*",
        "uk": "*Не знайдено жодного користувача, який дозволив пунгувати себе.*"
    }
    HOW_TO_PING_PINDABLE_USERS = {
        "en": "Type /here to ping only users who allow it.",
        "uk": "Скористайтеся /here, щоб відмітити всіх, хто дозволив пінгувати себе."
    }
    HOW_TO_ADD_USERS_TO_THE_LIST = {
        "en": "If anyone is not on the list, they just need to use any of my commands, and I'll them.",
        "uk": "Якщо когось немає у списку, вони можуть використати будь-яку з моїх команд, і я додам їх до своєї бази."
    }
    ONLY_ONE_USER_IN_GROUP = {
        "en": ("*It seems like you're the only one I know in this group right now.*\n\n"
               "To use /here or /everyone, I need to be familiar with at least one other person. "
               "Use /getmembers to see the list of everyone I know in this group."),
        "uk": ("*Здається, що наразі я знаю лише вас у цій групі.*\n\n"
               "Щоб використати /here або /everyone, мені потрібно знати хоча б ще одну людину. "
               "Використовуйте /getmembers, щоб побачити список усіх, кого я знаю в цій групі.")
    }
    NO_ONE_ALLOW_PINGING = {
        "en": ("*No one currently allows pinging.*\n\n"
               "To change this, use /pingme to enable pinging for yourself. "
               "You can also check /getmembers to see who has allowed or disabled pinging."),
        "uk": ("*Ніхто наразі не дозволив пінгування.*\n\n"
               "Щоб це змінити, скористайтеся /pingme, щоб дозволити пінгування для себе. "
               "Також можете переглянути /getmembers, щоб побачити, хто дозволив або заборонив пінгування.")
    }
    GET_ALL_ADMINS_LIST_TITLE = {
        "en": "*List of admins:*",
        "uk": "*Список адміністраторів групи:*"
    }
    HOW_TO_PING_ADMINS = {
        "en": ("Type /admins to ping all admins in group.\n"
               "_(Note: only admins can use this command.)_"),
        "uk": ("Скористайтеся /admins, щоб пінганути адмінів групи.\n"
               "_(Лише адміністратори можуть використовувати цю команду.)_")
    }
    ONLY_ADMINS_CAN_USE_THIS_COMMAND = {
        "en": "*Only admins can use this command.*",
        "uk": "*Ця команда доступна лише для адміністраторів.*"
    }
    NO_ADMINS_FOUND = {
        "en": "*No admins found.*",
        "uk": "*Не знайдено жодного адміна.*"
    }
