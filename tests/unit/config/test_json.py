"""
tests/unit/config/test_json.py
"""
import json
import os

from pygptprompt.config.json import dump_json, force_read_json, read_json, write_json


class TestJsonFunctions:
    def setup_method(self):
        self.file_path = "tests/test.temp.json"
        self.data = {"test": "data"}
        write_json(self.file_path, self.data)

    def teardown_method(self):
        # Clean up after each test by removing the file
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_read_json(self):
        assert read_json(self.file_path) == self.data

    def test_dump_json(self):
        assert dump_json(self.file_path) == json.dumps(self.data, indent=4)

    def test_write_json(self):
        assert read_json(self.file_path) == self.data

    def test_force_read_json(self):
        assert force_read_json(self.file_path, self.data) == self.data
        assert read_json(self.file_path) == self.data
