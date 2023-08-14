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
from typing import Any, Dict, List, Optional, Union

from pygptprompt import logging

# NOTE:
# List[Dict[str, Any]] uses a data type value of Any,
# enforcing generic types, to allow for portability.
JSONMap = Dict[str, Any]
JSONList = List[JSONMap]
JSONData = Union[JSONMap, JSONList]

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


class JSONTemplate:
    """
    A template class for working with JSON files.

    Properties:
        _file_path (Path): A path-like object pointing to the JSON source file.
        _data (Optional[JSONData]): The internal JSON data structure. May be None if not loaded.
    """

    def __init__(self, file_path: str, initial_data: Optional[JSONData] = None):
        """
        Initialize a JSONTemplate instance.

        Parameters:
            file_path (str): The path to the JSON file.
            initial_data (Optional[JSONData]): The initial data. Defaults to None.
        """
        self._file_path = Path(file_path)
        self._data: Optional[JSONData] = initial_data

        # Test for initialization data
        if initial_data is None:
            # Read the JSON data into memory
            loaded = self.load_json()
            if not loaded:
                raise ValueError("Failed to load JSON into memory")
            else:
                logging.info("JSON successfully loaded into memory")
        else:
            logging.info("JSON successfully initialized into memory")

    @property
    def file_path(self) -> Path:
        """
        Get the path to the JSON file.

        Returns:
            Path: The file path.
        """
        return self._file_path

    @property
    def data(self) -> JSONData:
        """
        Get the underlying JSON data structure.

        Returns:
            JSONData (Union[JSONMap, JSONList]): The underlying data structure.
        """
        return self._data

    def load_json(self) -> bool:
        """
        Load JSON data from the file into the _data attribute.

        Returns:
            bool: True if the JSON data was loaded successfully, False on error.
        """
        try:
            with self._file_path.open("r") as file:
                self._data = json.load(file)
            return True
        except DecodeError as e:
            logging.error(f"Error loading JSON from {self._file_path}: {e}")
            return False

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
