import json
import os
from pathlib import Path

from pygptprompt.pattern.mapping import JSONInterface


class TestMappingInterface:
    pass


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
