"""
pygptprompt/pattern/logger.py
"""
import logging
import sys

LOGGER_FORMAT = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"


def get_default_logger(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(LOGGER_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger
