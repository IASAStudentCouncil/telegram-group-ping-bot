import os
from dotenv import load_dotenv

# Loading variables from .env file
load_dotenv()

# Load bot variables
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot_name = os.getenv("TELEGRAM_BOT_NAME")

# Telegram API
telegram_api_id = os.getenv("TELEGRAM_API_ID")
telegram_api_hash = os.getenv("TELEGRAM_API_HASH")

# MongoDB
mongo_user = os.getenv("MONGO_USER_NAME")
mongo_pass = os.getenv("MONGO_USER_PASS")
mongo_host = os.getenv("MONGO_HOST")
mongo_params = os.getenv("MONGO_PARAMS")
mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_host}/?{mongo_params}"

db_name = os.getenv("MONGO_DB_NAME")

# Checking all enviroment variables
env_var = [
    bot_token, bot_name,
    telegram_api_id, telegram_api_hash,
    mongo_user, mongo_pass,
    mongo_host, mongo_params,
    db_name
]

if not all(env_var):
    raise EnvironmentError("One or more critical environment variables are missing!")

# Supported languages
available_languages = {
    "en": "EN🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "uk": "UA🇺🇦"
}

__all__ = ("mongo_uri", "db_name", "bot_token", "bot_name", "available_languages")
