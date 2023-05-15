import json
from typing import Any, Optional


def get_config(filepath: Optional[str] = None) -> dict[str, Any]:
    # Load the configuration
    filepath = filepath if filepath else "config.json"
    with open(filepath, "r") as f:
        config = json.load(f)
    return config
