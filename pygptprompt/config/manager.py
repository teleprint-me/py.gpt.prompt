"""
pygptprompt/config/manager.py
"""
import logging
import os
from logging import Logger
from pathlib import Path
from typing import Any, Optional

import dotenv

from pygptprompt.pattern.json import JSONMap
from pygptprompt.pattern.mapping import MappingTemplate
from pygptprompt.pattern.singleton import Singleton


class ConfigurationManager(Singleton):
    """
    Singleton class for managing configuration data.
    """

    def __init__(
        self,
        file_path: str,
        initial_data: Optional[JSONMap] = None,
        logger: Optional[Logger] = None,
    ):
        """
        Initialize the ConfigurationManager instance.

        Args:
            file_path (str): The path to the configuration file.
            initial_data (Optional[JSONMap], optional): Initial configuration data. Defaults to None.
        """
        super(ConfigurationManager, self).__init__()

        # Initialize the Configuration map
        self._map_template = MappingTemplate(
            file_path=file_path, initial_data=initial_data, logger=logger
        )
        self._map_template.load_json()

    def load(self) -> bool:
        """
        Load configuration data from the file.

        Returns:
            bool: True if the data was loaded successfully, False otherwise.
        """
        return self._map_template.load_json()

    def save(self) -> bool:
        """
        Save configuration data to the file.

        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        return self._map_template.save_json(self._map_template.data)

    def backup(self) -> bool:
        """
        Create a backup of the configuration file.

        Returns:
            bool: True if the backup was created successfully, False otherwise.
        """
        return self._map_template.backup_json()

    def get_value(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a configuration value based on the provided key.

        Args:
            key (str): The key to retrieve the value for.
            default (Optional[Any], optional): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The configuration value corresponding to the key, or the default value if not found.
        """
        keys = key.split(".")
        return self._map_template.read_nested(*keys) or default

    def set_value(self, key: str, value: Any) -> bool:
        """
        Set a configuration value for the provided key.

        Args:
            key (str): The key to set the value for.
            value (Any): The value to set.

        Returns:
            bool: True if the value was set successfully, False otherwise.
        """
        keys = key.split(".")
        return self._map_template.update_nested(value, *keys)

    def evaluate_path(self, key: str, default: Optional[Any] = None) -> Optional[str]:
        """
        Evaluate a configuration path based on the provided key.

        Args:
            key (str): The key to retrieve the path for.
            default (Optional[Any], optional): The default value to return if the path is not found. Defaults to None.

        Returns:
            Optional[str]: The evaluated path, or the default value if not found.
        """
        path = self.get_value(key, default)
        if path is None:
            return None
        if not isinstance(path, str):
            raise TypeError(f"Expected a string for path but got {type(path).__name__}")
        return os.path.expanduser(os.path.expandvars(path))

    def get_environment(self, variable: str = "OPENAI_API_KEY") -> str:
        """
        Get the value of an environment variable.

        Args:
            variable (str, optional): The name of the environment variable. Defaults to "OPENAI_API_KEY".

        Returns:
            str: The value of the environment variable.
        """
        env_path = self.evaluate_path("app.path.env", ".env")

        if not dotenv.load_dotenv(env_path):
            raise ValueError("EnvironmentError: Failed to load `.env`")

        value = os.getenv(variable) or ""

        if not value:
            raise ValueError(f"EnvironmentError: Failed to find `{variable}`")

        return value

    def get_logger(self, key: str, logger_name: str, level: str = "DEBUG") -> Logger:
        # Use cache path from config or fallback to '/tmp' or another path
        default_path = self.get_value("app.path.cache", "/tmp/pygptprompt/logs")

        log_file_path = self.evaluate_path(
            f"{key}.path",
            str(Path(default_path) / key),
        )

        log_level = self.get_value(f"{key}.level", level)

        logger = logging.getLogger(logger_name)

        if not logger.handlers:
            handler = logging.FileHandler(log_file_path, "a")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(log_level)

        return logger
