from datetime import datetime


class AdminMessages:
    """These messages are used for admin chat."""

    BOT_STARTUP_ADMIN_MESSAGE = {
        "en": f"*Bot started* ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n",
        "uk": f"*Бота запущено* ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n"
    }

    BOT_SHUTDOWN_ADMIN_MESSAGE = {
        "en": f"*Bot stopped* ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n",
        "uk": f"*Бота зупинено* ({datetime.now().strftime('%d-%m-%Y %H:%M:%S')})\n"
    }

    BOT_REPORT_MESSAGE = {
        "en": ("📊 *Bot {0} Report*\n\n"
               "- *Total Active Groups:* {1} \n"
               "- *{0} Message Sent:* {2}/{1} groups"),
        "uk": ("📊 *{0} Звіт*\n\n"
               "- *Кількість активних груп:* {1} \n"
               "- *'{0}' повідомлення надіслано:* {2} з {1}")
    }
