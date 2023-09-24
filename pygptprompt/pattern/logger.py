"""
pygptprompt/pattern/logger.py
"""
import logging
import sys

LOGGER_FORMAT = "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"


def get_default_logger(name=None, level=logging.DEBUG):
    """
    Get a default logger instance with specified configuration.

    This function retrieves or creates a default logger instance configured with the specified logger name and log level. If a logger with the same name already exists, it returns the existing logger; otherwise, it creates a new one.

    Args:
        name (str, optional): The name of the logger (default is None, which uses the root logger).
        level (int, optional): The log level for the logger (default is logging.DEBUG).

    Returns:
        Logger: A configured logger instance.

    Example:
        To get a default logger, you can use this function as follows:
        ```
        logger = get_default_logger("MyLogger", logging.INFO)
        logger.info("This is an info message.")
        ```

    Note:
        - If the logger with the specified `name` already exists, it returns the existing logger to ensure consistent logging across the application.
        - By default, log messages are written to the standard output (stdout), and the log format includes timestamp, filename, line number, log level, and the log message itself.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(LOGGER_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger
