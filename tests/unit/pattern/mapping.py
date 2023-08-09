"""
tests/unit/pattern/mapping.py
"""
import json
import os
from pathlib import Path

from pygptprompt.pattern.mapping import JSONInterface, MappingInterface


class TestMappingInterface:
    def setup_method(self, method):
        self.mapping_interface = MappingInterface(
            initial_data={"key1": "value1", "nested": {"key2": "value2"}}
        )

    def test_create(self):
        # Create a new key-value pair
        assert self.mapping_interface.create("new_key", "new_value") is True

        # Attempt to create the same key-value pair again (should return False since it already exists)
        assert self.mapping_interface.create("new_key", "new_value") is False

        # Check existing key-value pair
        assert self.mapping_interface.data["new_key"] == "new_value"

    def test_create_nested(self):
        assert (
            self.mapping_interface.create_nested("new_value", "nested", "key3") is True
        )
        assert self.mapping_interface.data["nested"]["key3"] == "new_value"

    def test_read(self):
        assert self.mapping_interface.read("key1") == "value1"

    def test_read_nested(self):
        assert self.mapping_interface.read_nested("nested", "key2") == "value2"

    def test_update(self):
        assert self.mapping_interface.update("key1", "updated_value") is True
        assert self.mapping_interface.data["key1"] == "updated_value"

    def test_update_nested(self):
        assert (
            self.mapping_interface.update_nested("updated_value", "nested", "key2")
            is True
        )
        assert self.mapping_interface.data["nested"]["key2"] == "updated_value"

    def test_delete(self):
        assert self.mapping_interface.delete("key1") is True
        assert "key1" not in self.mapping_interface.data

    def test_delete_nested(self):
        assert self.mapping_interface.delete_nested("nested", "key2") is True
        assert "key2" not in self.mapping_interface.data["nested"]

    def test_create_existing_key(self):
        assert self.mapping_interface.create("key1", "new_value") is False
        assert (
            self.mapping_interface.data["key1"] == "value1"
        )  # Ensure the existing value is not changed

    def test_read_nonexistent_key(self):
        assert self.mapping_interface.read("nonexistent_key") is None

    def test_read_nested_nonexistent_key(self):
        assert self.mapping_interface.read_nested("nested", "nonexistent_key") is None

    def test_update_and_create_behavior(self):
        # Update an existing key's value (should return True since the key exists)
        assert self.mapping_interface.update("new_key", "updated_value") is True

        # Read the value to ensure it was updated
        assert self.mapping_interface.read("new_key") == "updated_value"

        # Use update to create a new key-value pair (should return True since the key does not exist)
        assert self.mapping_interface.update("nonexistent_key", "new_value") is True

        # Read the newly created value to ensure it was created
        assert self.mapping_interface.read("nonexistent_key") == "new_value"

    def test_update_nested_nonexistent_key(self):
        assert (
            self.mapping_interface.update_nested(
                "new_value", "nested", "nonexistent_key"
            )
            is False
        )

    def test_delete_nonexistent_key(self):
        assert self.mapping_interface.delete("nonexistent_key") is False

    def test_delete_nested_nonexistent_key(self):
        assert (
            self.mapping_interface.delete_nested("nested", "nonexistent_key") is False
        )

    def test_nested_operations_with_non_dict(self):
        assert self.mapping_interface.read_nested("non_dict_key", "key") is None
        assert (
            self.mapping_interface.update_nested("new_value", "non_dict_key", "key")
            is False
        )
        assert self.mapping_interface.delete_nested("non_dict_key", "key") is False


class TestJSONInterface:
    def setup_method(self, method):
        self.json_filepath = Path("/tmp/test.json")
        self.data = {"test": "data"}
        # Ensure the file does not exist before each test
        if os.path.exists(self.json_filepath):
            os.remove(self.json_filepath)

    def teardown_method(self, method):
        # Clean up after each test by removing the file
        if os.path.exists(self.json_filepath):
            os.remove(self.json_filepath)

    def test_load_json(self, json_config):
        # Write the json_config data to the file path
        with open(self.json_filepath, "w") as f:
            json.dump(json_config, f)

        # Now, create the JSONInterface instance and try to load the data
        json_interface = JSONInterface(file_path=self.json_filepath)
        assert json_interface.load_json() == json_config

    def test_save_json(self, json_filepath):
        json_interface = JSONInterface(file_path=self.json_filepath)
        data_to_save = {"key": "value"}
        assert json_interface.save_json(data_to_save)
        # Validate file content by reading the file and comparing with data_to_save

    def test_backup_json(self, json_config):
        # Write the json_config data to the file path
        with open(self.json_filepath, "w") as f:
            json.dump(json_config, f)

        # Now, create the JSONInterface instance and try to backup the data
        json_interface = JSONInterface(file_path=self.json_filepath)
        assert json_interface.backup_json() is True

        # Verify that the backup file exists
        backup_path = self.json_filepath.with_suffix(".backup.json")
        assert os.path.exists(backup_path)

        # Optionally, you can also verify the contents of the backup file
        with open(backup_path, "r") as f:
            backup_data = json.load(f)
        assert backup_data == json_config

    def test_make_directory(self, tmpdir_factory):
        directory_path = str(tmpdir_factory.mktemp("new_directory"))
        file_path = os.path.join(directory_path, "file.json")
        json_interface = JSONInterface(file_path=file_path)
        assert json_interface.make_directory()
        assert os.path.exists(directory_path)


class TestJSONManager:
    pass
