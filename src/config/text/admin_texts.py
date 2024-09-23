class AdminMessages:
    """These messages are used for admin chat."""

    BOT_STARTUP_ADMIN_MESSAGE = {
        "en": "*Bot started* ({0})\n",
        "uk": "*Бота запущено* ({0})\n"
    }

    BOT_SHUTDOWN_ADMIN_MESSAGE = {
        "en": "*Bot stopped* ({0})\n",
        "uk": "*Бота зупинено* ({0})\n"
    }

    BOT_REPORT_MESSAGE = {
        "en": ("📊 *Bot {0} Report*\n\n"
               "- *Total Active Groups:* {1} \n"
               "- *{0} Message Sent:* {2}/{1} groups"),
        "uk": ("📊 *{0} Звіт*\n\n"
               "- *Кількість активних груп:* {1} \n"
               "- *'{0}' повідомлення надіслано:* {2} з {1}")
    }
