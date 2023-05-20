# pygptprompt/context/config.py
import json
import os
from typing import Any, Optional

import dotenv


def get_configuration(filepath: Optional[str] = None) -> dict[str, Any]:
    # Load the configuration
    filepath = filepath if filepath else "config.json"

    with open(filepath, "r") as f:
        config = json.load(f)

    if not config:
        raise ValueError("ConfigurationError: Failed to load `config.json`")

    return config


def get_api_key(config: dict[str, Any]) -> str:
    # Path to environment source
    env: str = config.get("environment_path", ".env")

    if not dotenv.load_dotenv(env):
        raise ValueError("EnvironmentError: Failed to load `.env`")

    api_key: str = os.getenv("OPENAI_API_KEY") or ""

    if not api_key:
        raise ValueError("EnvironmentError: Failed to load `OPENAI_API_KEY`")

    return api_key
