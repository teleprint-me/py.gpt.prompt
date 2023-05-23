# pygptprompt/config.py
import json
import os
from typing import Any, Optional, Union

import dotenv

from pygptprompt.singleton import Singleton


class Configuration(Singleton):
    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath if filepath else "config.json"
        self.config = self._load_configuration()

    def _load_configuration(self) -> dict[str, Any]:
        with open(self.filepath, "r") as f:
            config = json.load(f)

        if not config:
            raise ValueError("ConfigurationError: Failed to load `config.json`")

        return config

    def _get_value_by_key(
        self,
        data: Union[list[Any], dict[str, Any]],
        key: str,
    ) -> Any:
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            if key in data:
                return data[key]
            for val in data.values():
                result = self._get_value_by_key(val, key)
                if result is not None:
                    return result
        return None

    def get_api_key(self) -> str:
        env = self._get_value_by_key(self.config, "path.environment")

        if not dotenv.load_dotenv(env):
            raise ValueError("EnvironmentError: Failed to load `.env`")

        api_key = os.getenv("OPENAI_API_KEY") or ""

        if not api_key:
            raise ValueError("EnvironmentError: Failed to load `OPENAI_API_KEY`")

        return api_key

    def get_value(self, key: str, default: Optional[Any] = None) -> Any:
        return self._get_value_by_key(self.config, key) or default
