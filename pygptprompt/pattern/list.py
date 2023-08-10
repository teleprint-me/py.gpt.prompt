"""
pygptprompt/pattern/list.py
"""
from copy import deepcopy
from typing import Any, Dict, List, Optional


class ListTemplate:
    def __init__(self, initial_data: Optional[List[Dict[str, Any]]] = None):
        self._data = initial_data if initial_data is not None else []

    @property
    def length(self) -> int:
        """Return the length of the internal data list."""
        return len(self._data)

    @property
    def data(self) -> Optional[List[Dict[str, Any]]]:
        """Return a copy of the internal data list or None if empty."""
        return deepcopy(self._data) if self._data else None

    def observe(self, data: List[Dict[str, Any]]) -> None:
        """Update the underlying data structure with new data."""
        self._data = data

    def append(self, item: Dict[str, Any]) -> None:
        self._data.append(item)

    def insert(self, index: int, item: Dict[str, Any]) -> bool:
        if index < 0 or index > len(self._data):
            return False
        self._data.insert(index, item)
        return True

    def get(self, index: int) -> Optional[Dict[str, Any]]:
        return self._data[index] if 0 <= index < len(self._data) else None

    def update(self, index: int, item: Dict[str, Any]) -> bool:
        if index < 0 or index >= len(self._data):
            return False
        self._data[index] = item
        return True

    def remove(self, index: int) -> bool:
        if index < 0 or index >= len(self._data):
            return False
        del self._data[index]
        return True

    def clear(self) -> None:
        self._data.clear()
