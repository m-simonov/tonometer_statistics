import os

from dotenv import load_dotenv


load_dotenv()


BOT__TOKEN = os.environ["BOT__TOKEN"]
ADMINS__ID = os.environ["ADMINS__ID"]
DSN__DATABASE = os.environ["DSN__DATABASE"]

SYSTEM__DEBUG = bool(int(os.environ["SYSTEM__DEBUG"]))

LOGTAIL__TOKEN = os.environ["LOGTAIL__TOKEN"]
LOGTAIL__LEVEL = os.environ["LOGTAIL__LEVEL"]

LOGGER__LEVEL = os.environ["LOGGER__LEVEL"]
