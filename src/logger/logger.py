import sys

from logtail import LogtailHandler
from loguru import logger

from settings import LOGGER__LEVEL, LOGTAIL__TOKEN, LOGTAIL__LEVEL


logtail_handler = LogtailHandler(source_token=LOGTAIL__TOKEN)

logger.remove(0)

logger.add(
    sys.stderr,
    format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message} | {extra}",
    level=LOGGER__LEVEL,
    backtrace=False,
    diagnose=False,
)

logger.add(
    logtail_handler,
    format="{message}",
    level=LOGTAIL__LEVEL,
    backtrace=False,
    diagnose=False,
)
