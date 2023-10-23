"""
pygptprompt/json/utils.py
"""
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Union


def read_json(filepath: Union[str, Path]) -> Any:
    """
    Read JSON data from a file.

    Args:
        filepath (Union[str, Path]): The path to the JSON file.

    Returns:
        Any: The deserialized JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If there is an error decoding the JSON data.
    """
    with open(filepath, "r") as file:
        return json.load(file)


def dump_json(filepath: Union[str, Path]) -> str:
    """
    Serialize JSON data to a formatted string.

    Args:
        filepath (Union[str, Path]): The path to the JSON file.

    Returns:
        str: The serialized JSON data in a formatted string.
    """
    with open(filepath, "r") as file:
        return json.dumps(json.load(file), indent=4)


def write_json(filepath: Union[str, Path], content: Any) -> None:
    """
    Write JSON data to a file.

    Args:
        filepath (Union[str, Path]): The path to the JSON file.
        content (Any): The data to be serialized and written as JSON.
    """
    with open(filepath, "w") as f:
        json.dump(content, f)


def force_read_json(filepath: Union[str, Path], content: Any) -> Any:
    """
    Read JSON data from a file, or create the file with default content if it doesn't exist.

    If the specified file does not exist, it will be created with the provided content.
    This is useful for ensuring that a file exists before reading from it.

    Args:
        filepath (Union[str, Path]): The path to the JSON file.
        content (Any): The default content to be written as JSON if the file doesn't exist.

    Returns:
        Any: The deserialized JSON data.

    Raises:
        JSONDecodeError: If there is an error decoding the JSON data.
    """
    try:
        return read_json(filepath)
    except (FileNotFoundError, JSONDecodeError):
        write_json(filepath, content)
        return read_json(filepath)
