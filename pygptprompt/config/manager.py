"""
pygptprompt/config/manager.py
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional

import dotenv

from pygptprompt.config.path import evaluate_path
from pygptprompt.pattern.json import JSONTemplate
from pygptprompt.pattern.mapping import MappingTemplate
from pygptprompt.pattern.singleton import Singleton


class ConfigurationManager(Singleton):
    """Singleton class for managing configuration data using JSON files.

    Args:
        file_path (str): The path to the configuration JSON file.
        initial_data (Optional[Dict[str, Any]], optional): Initial configuration data. Defaults to None.

    Attributes:
        json_template (JSONInterface): Interface for interacting with the JSON file.
        map_template (MappingInterface): Interface for managing mapping data.
        file_path (Path): The pathlib.Path object representing the configuration file path.

    Methods:
        load() -> dict[str, Any]: Load configuration data from the JSON file.
        save() -> None: Save configuration data to the JSON file.
        backup() -> None: Create a backup copy of the JSON file.
        get_value(key: str, default: Optional[Any] = None) -> Any: Retrieve a configuration value.
        set_value(key: str, value: Any) -> bool: Set a configuration value.
        get_env_variable(env_var: str = "OPENAI_API_KEY") -> str: Get an environment variable value.
    """

    def __init__(self, file_path: str, initial_data: Optional[Dict[str, Any]] = None):
        """Initialize the ConfigurationManager.

        Args:
            file_path (str): The path to the configuration JSON file.
            initial_data (Optional[Dict[str, Any]], optional): Initial configuration data. Defaults to None.
        """
        super().__init__(file_path, initial_data)
        self.file_path = Path(file_path)
        self.json_template = JSONTemplate(file_path=file_path)
        self.mapping_template = MappingTemplate(initial_data=initial_data)
        self.json_template.register(self.mapping_template.observe)

    def load(self) -> dict[str, Any]:
        """Load configuration data from the JSON file.

        Returns:
            dict[str, Any]: The loaded configuration data.
        """
        return self.json_template.load_json()

    def save(self) -> None:
        """Save configuration data to the JSON file."""
        self.json_template.save_json(self.map_template.data)

    def backup(self) -> None:
        """Create a backup copy of the JSON file."""
        self.json_template.backup_json()

    def get_value(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a configuration value.

        Args:
            key (str): The configuration key.
            default (Optional[Any], optional): Default value if the key is not found. Defaults to None.

        Returns:
            Any: The retrieved configuration value or the default value if not found.
        """
        keys = key.split(".")
        return self.map_template.read_nested(*keys) or default

    def set_value(self, key: str, value: Any) -> bool:
        """Set a configuration value.

        Args:
            key (str): The configuration key.
            value (Any): The value to set.

        Returns:
            bool: True if the value was successfully set, False otherwise.
        """
        keys = key.split(".")
        return self.map_template.update_nested(value, *keys)

    def get_env_variable(self, env_var: str = "OPENAI_API_KEY") -> str:
        """Get an environment variable value.

        Args:
            env_var (str, optional): The name of the environment variable. Defaults to "OPENAI_API_KEY".

        Returns:
            str: The value of the environment variable.

        Raises:
            ValueError: If the environment variable is not found or cannot be loaded.
        """
        env = evaluate_path(self.get_value("app.path.env", ".env"))

        if not dotenv.load_dotenv(env):
            raise ValueError("EnvironmentError: Failed to load `.env`")

        value = os.getenv(env_var) or ""

        if not value:
            raise ValueError(f"EnvironmentError: Failed to load `{env_var}`")

        return value
