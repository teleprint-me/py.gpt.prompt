"""
pygptprompt/pattern/json.py

WARNING:
    Be cautious when parsing JSON data from untrusted sources. A malicious JSON string may cause the decoder to consume considerable CPU and memory resources. Limiting the size of data to be parsed is recommended.

REFERENCE:
    https://docs.python.org/3/library/json.html
    https://docs.python.org/3/library/exceptions.html
"""
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from pygptprompt import logging

EncodeError = (
    TypeError,  # raised by json.dump(s)
    FileNotFoundError,
    NotADirectoryError,
    PermissionError,
)

DecodeError = (
    json.JSONDecodeError,  # raised by json.load(s)
    FileNotFoundError,
    NotADirectoryError,
    PermissionError,
)

JSONError = EncodeError + DecodeError

# NOTE:
# List[Dict[str, Any]] uses a data type value of Any,
# enforcing generic types, to allow for portability.
JSONData = Union[Dict[str, Any], List[Dict[str, Any]]]


class JSONInterface:
    """
    A class for working with JSON files and providing callback support.
    """

    def __init__(self, file_path: str):
        """
        Initialize a JSONInterface instance.

        Parameters:
            file_path (str): The path to the JSON file.
        """
        self._file_path = Path(file_path)
        self._callbacks: List[Callable] = []

    @property
    def file_path(self) -> Union[str, Path]:
        """
        Get the path to the JSON file.

        Returns:
            Union[str, Path]: The file path.
        """
        return self._file_path

    def register(self, callback: Callable) -> None:
        """
        Register a callback function to be invoked on specific events.

        The callback system is designed with flexibility to allow for different signatures depending on the use case. This accommodates various requirements and makes the interface adaptable to different parts of the application.

        Example Callback Signatures:
            For MappingInterface: callback(data: Dict[str, Any]) -> None
            For ListInterface: callback(data: List[Dict[str, Any]]) -> None

        Parameters:
            callback (Callable): The function to register as a callback.
        """
        self._callbacks.append(callback)

    def load_json(self) -> Optional[Dict[str, Any]]:
        """
        Load JSON data from the file and notify registered callbacks.

        Returns:
            Optional[Dict[str, Any]]: The loaded JSON data or None on error.
        """
        try:
            with self._file_path.open("r") as file:
                data = json.load(file)
            # Notify all registered callbacks
            for callback in self._callbacks:
                callback(data)
            return data
        except DecodeError as e:
            logging.error(f"Error loading JSON from {self._file_path}: {e}")
            return None

    def save_json(self, data: JSONData) -> bool:
        """
        Save JSON data to the file.

        Parameters:
            data (JSONData): The data to be saved.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with self._file_path.open("w") as file:
                json.dump(data, file, indent=4)
            return True
        except EncodeError as e:
            logging.error(f"Error saving JSON to {self._file_path}: {e}")
            return False

    def backup_json(self) -> bool:
        """
        Create a backup of the JSON file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            backup_path = self._file_path.with_suffix(".backup.json")
            with self._file_path.open("r") as original_file, backup_path.open(
                "w"
            ) as backup_file:
                json.dump(json.load(original_file), backup_file, indent=4)
            return True
        except JSONError as e:
            logging.error(f"Error backing up JSON as {backup_path}: {e}")
            return False

    def make_directory(self) -> bool:
        """
        Create the directory for the JSON file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"Error creating path for {self._file_path}: {e}")
            return False
