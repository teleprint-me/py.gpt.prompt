"""
tests/unit/pattern/json.py
"""
import json
import os
from pathlib import Path


class TestJSONBaseTemplate:
    def test_json_file_path(self, json_base_template):
        assert json_base_template.file_path is not None
        assert isinstance(json_base_template.file_path, Path)

    def test_json_data(self, json_base_template):
        assert json_base_template.data is not None
        assert isinstance(json_base_template.data, dict)
        assert bool(json_base_template.data) is True

    def test_json_loading(self, json_base_template, temp_json_file):
        assert json_base_template.load_json() is True
        assert json_base_template.data.get("test") == "data"

    def test_json_saving(self, json_base_template, temp_json_file, temp_json_data):
        new_data = {"new": "data"}
        assert json_base_template.save_json(new_data) is True
        json_base_template.load_json()  # ensure the data persisted
        assert json_base_template.data == new_data

    def test_json_backup(
        self, json_base_template, temp_json_file, temp_json_backup_path
    ):
        assert json_base_template.backup_json() is True
        assert os.path.exists(temp_json_backup_path) is True
        with open(temp_json_file, "r") as original, open(
            temp_json_backup_path, "r"
        ) as backup:
            assert json.load(original) == json.load(backup)
        os.remove(temp_json_backup_path)  # Cleanup the backup file

    def test_json_directory_creation(
        self, json_base_template_nested, temp_json_nested_path
    ):
        dir_path = Path(temp_json_nested_path).parent
        if dir_path.exists():
            dir_path.rmdir()  # Ensure the directory doesn't exist before the test
        assert json_base_template_nested.make_directory() is True
        assert dir_path.exists() is True
