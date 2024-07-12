# Module that implements basic console logging.
# TODO: Log errors and warnings to a file.

import logging
from enum import Enum


class Level(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    DEBUG = 5


def init():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s     %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


# Log a message to the console.
def log(msg: str, level: Level = Level.INFO):
    match level:
        case Level.INFO:
            logging.info(msg)
        case Level.WARNING:
            logging.warning(msg)
        case Level.ERROR:
            logging.error(msg)
        case Level.CRITICAL:
            logging.critical(msg)
        case Level.DEBUG:
            logging.debug(msg)
