# pygptprompt/config.py
import json
import os
from typing import Any, Optional, Union

import dotenv

from pygptprompt.singleton import Singleton


class Configuration(Singleton):
    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath if filepath else "config.json"
        self.data = self.load()

    def load(self) -> dict[str, Any]:
        with open(self.filepath, "r") as f:
            config = json.load(f)

        if not config:
            raise ValueError("ConfigurationError: Failed to load `config.json`")

        return config

    def get_value_by_key(
        self,
        data: Union[list[Any], dict[str, Any]],
        key: str,
        exact_path: bool = False,
    ) -> Any:
        if exact_path:
            keys = key.split(".")
            for key in keys:
                if isinstance(data, dict) and key in data:
                    data = data[key]
                else:
                    return None
            return data
        else:
            if isinstance(data, dict):
                if key in data:
                    return data[key]
                for val in data.values():
                    if isinstance(val, dict):
                        result = self.get_value_by_key(val, key)
                        if result is not None:
                            return result
        return None

    def get_value(self, key: str, default: Optional[Any] = None) -> Any:
        keys = key.split(".")
        data = self.data

        for key in keys:
            data = self.get_value_by_key(data, key, exact_path=True)

            if data is None:
                return default

        return data

    def get_api_key(self) -> str:
        env = self.get_value("path.environment", ".env")

        if not dotenv.load_dotenv(env):
            raise ValueError("EnvironmentError: Failed to load `.env`")

        api_key = os.getenv("OPENAI_API_KEY") or ""

        if not api_key:
            raise ValueError("EnvironmentError: Failed to load `OPENAI_API_KEY`")

        return api_key
