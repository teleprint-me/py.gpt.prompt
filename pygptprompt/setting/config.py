# pygptprompt/setting/config.py
import datetime
import os
import shutil
from pathlib import Path
from typing import Any, Optional

import dotenv

from pygptprompt.pattern import MappingTemplate, Singleton
from pygptprompt.setting.json import read_json, write_json


class GlobalConfiguration(Singleton, MappingTemplate):
    def __init__(self, filepath: Optional[str] = None):
        super()
        self.filepath = Path(filepath if filepath else "config.json")
        self._data = self.load()

    def load(self) -> dict[str, Any]:
        return read_json(self.filepath)

    def save(self) -> None:
        write_json(self.filepath, self.data)

    def backup(self) -> None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.filepath.name.replace(".json", f"_{timestamp}.json")
        backup_filename = self.filepath.parent / filename
        shutil.copyfile(self.filepath, backup_filename)

    def get_value(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> Any:
        keys = key.split(".")
        data = self.read_nested(*keys)
        return data if data is not None else default

    def get_api_key(self) -> str:
        env = self.get_value("path.environment", ".env")

        if not dotenv.load_dotenv(env):
            raise ValueError("EnvironmentError: Failed to load `.env`")

        api_key = os.getenv("OPENAI_API_KEY") or ""

        if not api_key:
            raise ValueError("EnvironmentError: Failed to load `OPENAI_API_KEY`")

        return api_key
