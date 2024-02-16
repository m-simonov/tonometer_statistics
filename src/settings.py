import os

from dotenv import load_dotenv


load_dotenv()


BOT__TOKEN = os.environ.get("BOT__TOKEN")
ADMINS__ID = os.environ.get("ADMINS__ID")
DSN__DATABASE = os.environ.get("DSN__DATABASE")

SYSTEM__DEBUG = bool(int(os.environ.get("SYSTEM__DEBUG")))
