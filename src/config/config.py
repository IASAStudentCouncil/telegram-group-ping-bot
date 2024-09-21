import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot configuration
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot_name = os.getenv("TELEGRAM_BOT_NAME")

# Admin configuration
admin_chat_id = int(os.getenv("ADMIN_CHAT_ID"))

# Telegram API configuration
telegram_api_id = os.getenv("TELEGRAM_API_ID")
telegram_api_hash = os.getenv("TELEGRAM_API_HASH")

# MongoDB configuration
mongo_user = os.getenv("MONGO_USER_NAME")
mongo_pass = os.getenv("MONGO_USER_PASS")
mongo_host = os.getenv("MONGO_HOST")
mongo_params = os.getenv("MONGO_PARAMS")
mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_host}/?{mongo_params}"

db_name = os.getenv("MONGO_DB_NAME")

# Ensure all critical environment variables are present
required_env_vars = {
    "TELEGRAM_BOT_TOKEN": bot_token,
    "TELEGRAM_BOT_NAME": bot_name,
    "ADMIN_CHAT_ID": admin_chat_id,
    "TELEGRAM_API_ID": telegram_api_id,
    "TELEGRAM_API_HASH": telegram_api_hash,
    "MONGO_USER_NAME": mongo_user,
    "MONGO_USER_PASS": mongo_pass,
    "MONGO_HOST": mongo_host,
    "MONGO_PARAMS": mongo_params,
    "MONGO_DB_NAME": db_name
}

missing_vars = [key for key, value in required_env_vars.items() if not value]
if missing_vars:
    raise OSError(f"Missing critical environment variables: {', '.join(missing_vars)}")

# Supported languages
available_languages = {
    "en": "EN🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "uk": "UA🇺🇦"
}

__all__ = (
    "mongo_uri", "db_name",
    "bot_token", "bot_name", "admin_chat_id",
    "telegram_api_id", "telegram_api_hash",
    "available_languages"
)
