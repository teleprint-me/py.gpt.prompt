# pygptprompt/setting/json.py
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Union


def read_json(filepath: Union[str, Path]) -> Any:
    with open(filepath, "r") as file:
        return json.load(file)


def dump_json(filepath: Union[str, Path]) -> str:
    with open(filepath, "r") as file:
        return json.dumps(json.load(file), indent=4)


def write_json(filepath: Union[str, Path], content: Any) -> None:
    with open(filepath, "w") as f:
        json.dump(content, f)


def force_read_json(filepath: Union[str, Path], content: Any) -> Any:
    try:
        return read_json(filepath)
    except (FileNotFoundError, JSONDecodeError):
        write_json(filepath, content)
        return read_json(filepath)
