# Dictionary to store text for group messages
class GroupMessages:
    START = {
        "en": "Hey! I'm *Ping Bot* 😊\n\n"
              "Type /help to explore all my commands.",
        "uk": "Привіт! Я — *Ping Bot* 😊\n\n"
              "Використовуйте /help, щоб ознайомитись з усіма моїми командами."
    }
    HELP = {
        "en": "I can help you ping members in your group quickly, like in Discord. "
              "Here are some commands you can use:\n\n"
              "/language - change the group chat language.\n"
              "/pingme - allow yourself to be pinged.\n"
              "/dontpingme - disable pings for yourself.\n"
              "/here - ping only users who allowed it.\n"
              "/everyone - ping all users.\n"
              "/getmembers - get a list of all users in the group, that I know.",
        "uk": "Я допоможу вам швидко відмічати учасників у вашій групі. "
              "Ось команди, які ви можете використовувати:\n\n"
              "/language - змінити мову групового чату.\n"
              "/pingme - дозволити пінгувати себе.\n"
              "/dontpingme - заборонити пінгувати себе.\n"
              "/here - відмітити тільки тих, хто дозволив пінгувати себе.\n"
              "/everyone - відмітити абсолютно всіх учасників.\n"
              "/getmembers - список всіх учасників групи, які мені відомі."
    }
    PARSING_USERS = {
        "en": "Adding all users to my database...",
        "uk": "Додаю усіх користувачів до бази даних..."
    }
    ADD_USER = {
        "en": "Welcome to the group! I'm *Ping Bot* 😊\n"
              "Type /help to learn how to use me.",
        "uk": "Ласкаво просимо до групи! Я — *Ping Bot* 😊\n"
              "Напишіть /help, щоб дізнатися, як користуватись мною."
    }
    DELETE_USER = {
        "en": "Goodbye! 😣",
        "uk": "Прощавайте! 😣"
    }
    CHOICE_LANGUAGE = {
        "en": "Choice language...",
        "uk": "Оберіть мову..."
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
    GET_ALL_PINGABLE_USERS = {
        "en": "*Able to be pinged:*",
        "uk": "*Користувачі, яких я можу пінгувати:*"
    }
    GET_ALL_UNPINGABLE_USERS = {
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
        "en": "*It seems like you're the only one I know in this group right now.*\n\n"
              "To use /here or /everyone, I need to be familiar with at least one other person. "
              "Use /getmembers to see the list of everyone I know in this group.",
        "uk": "*Здається, що наразі я знаю лише вас у цій групі.*\n\n"
              "Щоб використати /here або /everyone, мені потрібно знати хоча б ще одну людину. "
              "Використовуйте /getmembers, щоб побачити список усіх, кого я знаю в цій групі."
    }
    NO_ONE_ALLOW_PINGING = {
        "en": "*No one currently allows pinging.*\n\n"
              "To change this, use /pingme to enable pinging for yourself. "
              "You can also check /getmembers to see who has allowed or disabled pinging.",
        "uk": "*Ніхто наразі не дозволив пінгування.*\n\n"
              "Щоб це змінити, скористайтеся /pingme, щоб дозволити пінгування для себе. "
              "Також можете переглянути /getmembers, щоб побачити, хто дозволив або заборонив пінгування."
    }
