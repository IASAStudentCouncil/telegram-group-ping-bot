import os
from dotenv import load_dotenv

# Loading variables from .env file
load_dotenv()

# Load bot variables
bot_token = os.getenv("BOT_TOKEN")
bot_name = os.getenv("BOT_NAME")

# MongoDB
mongo_user = os.getenv("USER_NAME")
mongo_pass = os.getenv("USER_PASS")
mongo_host = os.getenv("MONGO_HOST")
mongo_params = os.getenv("MONGO_PARAMS")
mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_host}/?{mongo_params}"

db_name = os.getenv("DB_NAME")

# Checking all enviroment variables
env_var = [
    bot_token, bot_name,
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
