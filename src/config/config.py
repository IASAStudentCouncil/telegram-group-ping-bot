import os
from dotenv import load_dotenv

load_dotenv()

# ------ load tokens ---------
bot_token = os.getenv("BOT_TOKEN")
test_token = os.getenv("TEST_BOT_TOKEN")

# ------ connect to mongodb ---------
mongo_user = os.getenv("USER_NAME")
mongo_pass = os.getenv("USER_PASS")
mongo_host = "iasacluster.t0d4s.mongodb.net"
mongo_params = "retryWrites=true&w=majority&appName=IASAcluster"
mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_host}/?{mongo_params}"

if not all([bot_token, test_token, mongo_user, mongo_pass]):
    raise EnvironmentError("One or more critical environment variables are missing!")

__all__ = ("mongo_uri", "bot_token", "test_token")
