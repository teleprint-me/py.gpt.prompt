"""Template Method Design Pattern"""
from typing import Any, Optional


class MappingTemplate:
    def __init__(self, initial_data: Optional[dict[str, Any]] = None):
        self._dataset = initial_data if initial_data is not None else {}

    @property
    def keys(self) -> list[str]:
        return list(self._dataset.keys())

    @property
    def data(self) -> dict[str, Any]:
        return self._dataset

    def create(self, key: str, value: Any) -> bool:
        if key not in self._dataset:
            self._dataset[key] = value
            return True
        else:
            return False

    def create_nested(self, value: Any, *keys: str) -> bool:
        data = self._dataset
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
        return self._dataset.get(key, None)

    def read_nested(self, *keys: str) -> Any:
        data = self._dataset
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data.get(key, None)
            else:
                return None
        return data

    def update(self, key: str, value: Any) -> bool:
        if key in self._dataset:
            self._dataset[key] = value
            return True
        else:
            return self.create(key, value)

    def update_nested(self, value: Any, *keys: str) -> bool:
        data = self._dataset
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
        if key in self._dataset:
            del self._dataset[key]
            return True
        else:
            return False

    def delete_nested(self, *keys: str) -> bool:
        data = self._dataset
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
