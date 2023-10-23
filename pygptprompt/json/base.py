"""
pygptprompt/json/base.py

WARNING:
    Be cautious when parsing JSON data from untrusted sources. A malicious JSON string may cause the decoder to consume considerable CPU and memory resources. Limiting the size of data to be parsed is recommended.

REFERENCE:
    https://docs.python.org/3/library/json.html
    https://docs.python.org/3/library/exceptions.html
"""
import json
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union

from pygptprompt.pattern.logger import get_default_logger

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


class JSONBaseTemplate(Protocol):
    """
    A base template class for working with JSON files.

    Properties:
        _file_path (Path): A path-like object pointing to the JSON source file.
        _data (Optional[JSONData]): The internal JSON data structure. May be None if not loaded.
        _logger (Optional[Logger]): Optional logger for error-handling.
    """

    def __init__(
        self,
        file_path: str,
        initial_data: Optional[JSONData] = None,
        logger: Optional[Logger] = None,
    ):
        """
        Initialize a JSONTemplate instance.

        Parameters:
            file_path (str): The path to the JSON file.
            initial_data (Optional[JSONData]): The initial data. Defaults to None.
            logger (Optional[Logger]): Optional logger for error-handling.
        """
        self._file_path = Path(file_path)
        self._data: Optional[JSONData] = initial_data

        if logger:
            self._logger = logger
        else:
            self._logger = get_default_logger(self.__class__.__name__)

        # Test for initialization data
        if initial_data is not None:
            self._logger.debug("JSON successfully initialized into memory")

    @property
    def file_path(self) -> Path:
        """
        Get the path to the JSON file.

        Returns:
            Path: The file path.
        """
        return self._file_path

    @property
    def data(self) -> Optional[JSONData]:
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
            bool: True if the JSON data was loaded successfully, False otherwise.
        """
        try:
            with self._file_path.open("r") as file:
                self._data = json.load(file)
            self._logger.debug(f"JSON successfully loaded from {self._file_path}")
            return True
        except DecodeError as e:
            self._logger.error(f"Error loading JSON from {self._file_path}: {e}")
            return False

    def save_json(self, data: Optional[JSONData] = None, indent: int = 4) -> bool:
        """
        Save JSON data to the file.

        If data is provided, it updates the _data attribute as well.

        Parameters:
            data (Optional[JSONData]): The data to be saved. Defaults to None.
            indent (int): The indentation level for the JSON output. Defaults to 4.

        Returns:
            bool: True if the JSON data was saved successfully, False otherwise.
        """
        try:
            with self._file_path.open("w") as file:
                if data is not None:
                    json.dump(data, file, indent=indent)
                    self._data = data  # Update the _data attribute if data is provided
                else:
                    json.dump(self._data, file, indent=indent)

            self._logger.debug(f"JSON successfully saved to {self._file_path}")
            return True
        except EncodeError as e:
            self._logger.error(f"Error saving JSON to {self._file_path}: {e}")
            return False

    def backup_json(self, indent: int = 4) -> bool:
        """
        Create a backup of the JSON file.

        Parameters:
            indent (int): The indentation level for the JSON output. Defaults to 4.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            backup_path = self._file_path.with_suffix(".backup.json")
            with self._file_path.open("r") as original_file, backup_path.open(
                "w"
            ) as backup_file:
                json.dump(json.load(original_file), backup_file, indent=indent)
            self._logger.debug(f"JSON successfully backed up to {backup_path}")
            return True
        except JSONError as e:
            self._logger.error(f"Error backing up JSON as {backup_path}: {e}")
            return False

    def make_directory(self) -> bool:
        """
        Create the directory for the JSON file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            self._logger.debug(f"Successfully created path for {self._file_path}")
            return True
        except (PermissionError, FileExistsError) as e:
            self._logger.error(f"Error creating path for {self._file_path}: {e}")
            return False
