"""
pygptprompt/pattern/mapping.py
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union


class JSONInterface:
    """Interface for interacting with JSON files.

    Args:
        file_path (str): The path to the JSON file.

    Attributes:
        _file_path (Path): The pathlib.Path object representing the file path.

    Methods:
        load_json(): Load JSON data from the file.
        save_json(data: Dict[str, Any]) -> bool: Save data to the JSON file.
        backup_json() -> bool: Create a backup copy of the JSON file.
        make_directory() -> bool: Create the directory for the file if it doesn't exist.
    """

    def __init__(self, file_path: str):
        """Initialize the JSONInterface with a file path."""
        self._file_path = Path(file_path)

    @property
    def file_path(self) -> Union[str, Path]:
        """Get the file path as a pathlib.Path object."""
        return self._file_path

    def load_json(self) -> Dict[str, Any]:
        """Load JSON data from the file.

        Returns:
            Dict[str, Any]: The loaded JSON data.
        """
        with open(self._file_path, "r") as file:
            return json.load(file)

    def save_json(self, data: Dict[str, Any]) -> bool:
        """Save data to the JSON file.

        Args:
            data (Dict[str, Any]): The data to be saved.

        Returns:
            bool: True if the data was successfully saved, False otherwise.
        """
        try:
            with self._file_path.open("w") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def backup_json(self) -> bool:
        """Create a backup copy of the JSON file.

        Returns:
            bool: True if the backup was created successfully, False otherwise.
        """
        try:
            backup_path = self._file_path.with_suffix(".backup.json")
            with self._file_path.open("r") as original_file, backup_path.open(
                "w"
            ) as backup_file:
                json.dump(json.load(original_file), backup_file, indent=4)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def make_directory(self) -> bool:
        """Create the directory for the file if it doesn't exist.

        Returns:
            bool: True if the directory was created successfully or already exists, False otherwise.
        """
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


class MappingInterface:
    """
    A template class for creating and managing a mapping of key-value pairs.

    Args:
        initial_data (Optional[dict[str, Any]]): Optional initial data to populate the mapping.

    Attributes:
        _data (dict[str, Any]): The underlying data structure for storing the key-value pairs.
    """

    def __init__(self, initial_data: Optional[dict[str, Any]] = None):
        self._data = initial_data if initial_data is not None else {}

    @property
    def keys(self) -> list[str]:
        """
        Get a list of all keys in the mapping.

        Returns:
            list[str]: A list of keys in the mapping.
        """
        return list(self._data.keys())

    @property
    def data(self) -> dict[str, Any]:
        """
        Get the underlying data structure of the mapping.

        Returns:
            dict[str, Any]: The underlying data structure.
        """
        return self._data

    def create(self, key: str, value: Any) -> bool:
        """
        Create a new key-value pair in the mapping.

        Args:
            key (str): The key of the pair.
            value (Any): The value of the pair.

        Returns:
            bool: True if the key-value pair was created successfully, False if the key already exists.
        """
        if key not in self._data:
            self._data[key] = value
            return True
        else:
            return False

    def create_nested(self, value: Any, *keys: str) -> bool:
        """
        Create a nested key-value pair in the mapping.

        Args:
            value (Any): The value of the pair.
            keys (str): The keys hierarchy for the nested pair.

        Returns:
            bool: True if the nested key-value pair was created successfully, False if any key in the hierarchy is missing or if the final key already exists.
        """
        data = self._data
        last_key = keys[-1]
        keys = keys[:-1]

        for key in keys:
            if isinstance(data, dict):
                data = data.setdefault(key, {})
            else:
                return False

        if last_key not in data:
            data[last_key] = value
            return True
        else:
            return False

    def read(self, key: str) -> Any:
        """
        Read the value associated with a key in the mapping.

        Args:
            key (str): The key to read the value from.

        Returns:
            Any: The value associated with the key, or None if the key is not present in the mapping.
        """
        return self._data.get(key, None)

    def read_nested(self, *keys: str) -> Any:
        """
        Read the value associated with a nested key hierarchy in the mapping.

        Args:
            keys (str): The keys hierarchy for the nested value.

        Returns:
            Any: The value associated with the nested keys hierarchy, or None if any key in the hierarchy is missing.
        """
        data = self._data
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data.get(key, None)
            else:
                return None
        return data

    def update(self, key: str, value: Any) -> bool:
        """
        Update the value associated with a key in the mapping.

        If the key is already present in the mapping, the value is updated. Otherwise, a new key-value pair is created.

        Args:
            key (str): The key to update or create.
            value (Any): The value to associate with the key.

        Returns:
            bool: True if the value was updated, False if a new key-value pair was created.
        """
        if key in self._data:
            self._data[key] = value
            return True
        else:
            return self.create(key, value)

    def update_nested(self, value: Any, *keys: str) -> bool:
        """
        Update the value associated with a nested key hierarchy in the mapping.

        If the nested keys hierarchy is already present in the mapping, the value is updated. Otherwise, a new nested key-value pair is created.

        Args:
            value (Any): The value to associate with the nested keys hierarchy.
            keys (str): The keys hierarchy for the nested value.

        Returns:
            bool: True if the value was updated, False if a new nested key-value pair was created.
        """
        data = self._data
        last_key = keys[-1]
        keys = keys[:-1]

        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return False

        if isinstance(data, dict) and last_key in data:
            data[last_key] = value
            return True
        else:
            return self.create_nested(value, *keys)

    def delete(self, key: str) -> bool:
        """
        Delete a key-value pair from the mapping.

        Args:
            key (str): The key to delete.

        Returns:
            bool: True if the key-value pair was deleted successfully, False if the key is not present in the mapping.
        """
        if key in self._data:
            del self._data[key]
            return True
        else:
            return False

    def delete_nested(self, *keys: str) -> bool:
        """
        Delete a nested key-value pair from the mapping.

        Args:
            keys (str): The keys hierarchy for the nested value.

        Returns:
            bool: True if the nested key-value pair was deleted successfully, False if any key in the hierarchy is missing.
        """
        data = self._data
        last_key = keys[-1]
        keys = keys[:-1]

        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return False

        if isinstance(data, dict) and last_key in data:
            del data[last_key]
            return True
        else:
            return False


class JSONManager:
    """Manager class for coordinating interactions with JSON files and mapping data.

    Args:
        file_path (str): The path to the JSON file.
        initial_data (Optional[Dict[str, Any]], optional): Initial data to populate the mapping interface. Defaults to None.

    Attributes:
        json_interface (JSONInterface): Interface for interacting with the JSON file.
        map_interface (MappingInterface): Interface for managing mapping data.

    Methods:
        __init__(file_path: str, initial_data: Optional[Dict[str, Any]] = None): Initialize the JSONManager.
    """

    def __init__(self, file_path: str, initial_data: Optional[Dict[str, Any]] = None):
        """Initialize the JSONManager.

        Args:
            file_path (str): The path to the JSON file.
            initial_data (Optional[Dict[str, Any]], optional): Initial data to populate the mapping interface. Defaults to None.
        """
        self.json_interface = JSONInterface(file_path)

        # Load data if JSON file exists, otherwise use initial_data
        if self.json_interface.file_path.exists():
            data = self.json_interface.load_json()
        else:
            # Create the directory for the file if it doesn't exist
            self.json_interface.make_directory()
            data = initial_data
            # Save initial data if provided
            if initial_data:
                self.json_interface.save_json(initial_data)

        # Initialize the mapping interface with either loaded data or initial data
        self.map_interface = MappingInterface(data)
