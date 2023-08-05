"""
pygptprompt/config/manager.py
"""
import datetime
import os
import shutil
from pathlib import Path
from typing import Any, Optional

import dotenv

from pygptprompt.config.json import read_json, write_json
from pygptprompt.config.path import evaluate_path
from pygptprompt.pattern.mapping import MappingTemplate
from pygptprompt.pattern.singleton import Singleton


class ConfigurationManager(Singleton, MappingTemplate):
    """
    Singleton class for managing global configuration settings.

    This class inherits from `Singleton` and `MappingTemplate` to implement the Singleton pattern
    and provide key-value mapping functionality for configuration settings.

    Args:
        file_path (str): The path to the configuration file.

    Attributes:
        file_path (Path): The path to the configuration file.
        _data (dict): The underlying data structure for storing the configuration settings.
    """

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = Path(file_path)
        self._data = self.load()

    def load(self) -> dict[str, Any]:
        """
        Load the configuration settings from the configuration file.

        Returns:
            dict[str, Any]: The loaded configuration settings.
        """
        return read_json(self.file_path)

    def save(self) -> None:
        """
        Save the configuration settings to the configuration file.
        """
        write_json(self.file_path, self.data)

    def backup(self) -> None:
        """
        Create a backup of the configuration file.

        The backup file will have the same name as the original file, with a timestamp appended to it.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = self.file_path.name.replace(".json", f"_{timestamp}.json")
        backup_file_name = self.file_path.parent / file_name
        shutil.copyfile(self.file_path, backup_file_name)

    def get_value(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> Any:
        """
        Get the value associated with a configuration key.

        The key can be a nested key, with each level separated by a dot ('.').
        If the key is not found, the default value is returned.

        Args:
            key (str): The configuration key.
            default (Optional[Any]): The default value to return if the key is not found. Defaults to None.

        Returns:
            Any: The value associated with the key, or the default value if the key is not found.
        """
        keys = key.split(".")
        data = self.read_nested(*keys)
        return data if data is not None else default

    def set_value(self, key: str, value: Any) -> bool:
        """
        Set or update the value associated with a configuration key.

        The key can be a nested key, with each level separated by a dot ('.').
        If the key hierarchy exists, the value is updated; otherwise, a new nested key-value pair is created.

        Args:
            key (str): The configuration key.
            value (Any): The value to set or update for the given key.

        Returns:
            bool: True if the value was updated, False if a new nested key-value pair was created.
        """
        keys = key.split(".")
        return self.update_nested(value, *keys)

    def get_api_key(self) -> str:
        """
        Get the OpenAI API key from the environment.

        The API key is read from the `.env` file specified in the configuration settings.
        If the API key is not found or empty, an error is raised.

        Returns:
            str: The OpenAI API key.

        Raises:
            ValueError: If the `.env` file cannot be loaded or the `OPENAI_API_KEY` environment variable is not set.
        """
        env = evaluate_path(self.get_value("app.path.env", ".env"))

        if not dotenv.load_dotenv(env):
            raise ValueError("EnvironmentError: Failed to load `.env`")

        api_key = os.getenv("OPENAI_API_KEY") or ""

        if not api_key:
            raise ValueError("EnvironmentError: Failed to load `OPENAI_API_KEY`")

        return api_key
