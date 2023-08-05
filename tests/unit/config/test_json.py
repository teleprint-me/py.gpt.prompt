"""
tests/unit/config/test_json.py
"""
import json
import os

from pygptprompt.config.json import dump_json, force_read_json, read_json, write_json


class TestJsonFunctions:
    def setup_method(self, method):
        self.json_filepath = "/tmp/test.json"
        self.data = {"test": "data"}
        # Ensure the file does not exist before each test
        if os.path.exists(self.json_filepath):
            os.remove(self.json_filepath)

    def teardown_method(self, method):
        # Clean up after each test by removing the file
        if os.path.exists(self.json_filepath):
            os.remove(self.json_filepath)

    def test_read_json(self):
        write_json(self.json_filepath, self.data)
        assert read_json(self.json_filepath) == self.data

    def test_dump_json(self):
        write_json(self.json_filepath, self.data)
        assert dump_json(self.json_filepath) == json.dumps(self.data, indent=4)

    def test_write_json(self):
        write_json(self.json_filepath, self.data)
        assert read_json(self.json_filepath) == self.data

    def test_force_read_json(self):
        assert force_read_json(self.json_filepath, self.data) == self.data
        assert read_json(self.json_filepath) == self.data
