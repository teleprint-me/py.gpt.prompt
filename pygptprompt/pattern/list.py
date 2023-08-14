"""
pygptprompt/pattern/list.py
"""
from copy import deepcopy
from typing import Optional

from pygptprompt.pattern.json import JSONList, JSONMap, JSONTemplate


class ListTemplate(JSONTemplate):
    """
    A template class for managing a list of dictionaries in JSON files.

    Properties:
        _file_path (Path): The file path of the JSON file.
        _data (JSONList): The underlying data structure for storing dictionaries. Uses initial_data if not None, otherwise loads JSON data from file_path. Raises an error if no data is given.
    """

    def __init__(self, file_path: str, initial_data: Optional[JSONList] = None):
        """
        Initialize a ListTemplate instance.

        Args:
            file_path (str): The path to the JSON file that stores the list.
            initial_data (Optional[JSONList]): Optional initial data to populate the list.
        """
        super(ListTemplate, self).__init__(file_path, deepcopy(initial_data))

    @property
    def length(self) -> int:
        """Return the length of the internal data list."""
        return len(self._data)

    @property
    def data(self) -> Optional[JSONList]:
        """Return a copy of the internal data list or None if empty."""
        return deepcopy(self._data) if self._data else None

    def append(self, item: JSONMap) -> None:
        """
        Append a dictionary to the internal data list.

        Parameters:
            item (JSONMap): The dictionary to append to the internal list.

        Returns:
            None
        """
        self._data.append(item)

    def insert(self, index: int, item: JSONMap) -> bool:
        """
        Insert a dictionary at a specific index.

        Parameters:
            index (int): The index at which to insert the dictionary.
            item (JSONMap): The dictionary to insert.

        Returns:
            bool: True if successful, False otherwise.
        """
        if index < 0 or index > len(self._data):
            return False
        self._data.insert(index, item)
        return True

    def get(self, index: int) -> Optional[JSONMap]:
        """
        Get a dictionary at a specific index.

        Parameters:
            index (int): The index of the dictionary to retrieve.

        Returns:
            Optional[JSONMap]: The dictionary at the specified index or None if index is out of range.
        """
        return self._data[index] if 0 <= index < len(self._data) else None

    def update(self, index: int, item: JSONMap) -> bool:
        """
        Update a dictionary at a specific index.

        Parameters:
            index (int): The index of the dictionary to update.
            item (JSONMap): The dictionary with updated values.

        Returns:
            bool: True if successful, False otherwise.
        """
        if index < 0 or index >= len(self._data):
            return False
        self._data[index] = item
        return True

    def remove(self, index: int) -> bool:
        """
        Remove a dictionary at a specific index.

        Parameters:
            index (int): The index of the dictionary to remove.

        Returns:
            bool: True if successful, False otherwise.
        """
        if index < 0 or index >= len(self._data):
            return False
        del self._data[index]
        return True

    def pop(self, index: int) -> Optional[JSONMap]:
        """
        Remove and return a dictionary at a specific index.

        Parameters:
            index (int): The index of the dictionary to pop.

        Returns:
            JSONMap: A dictionary if successful, None otherwise.
        """
        if index < 0 or index >= len(self._data):
            return None
        return self._data.pop(index)

    def clear(self) -> None:
        """Clear the internal data list."""
        self._data.clear()
