# tests/unit/test_config.py
import json
import os

import pytest

from pygptprompt.pattern import MappingTemplate, Singleton
from pygptprompt.setting import GlobalConfiguration


class TestConfiguration:
    def test_types(self, config: GlobalConfiguration):
        assert isinstance(config, Singleton)
        assert isinstance(config, MappingTemplate)
        assert isinstance(config, GlobalConfiguration)

    def test_attributes(self, config: GlobalConfiguration):
        assert hasattr(config, "filepath")
        assert hasattr(config, "_data")
        assert hasattr(config, "load")
        assert hasattr(config, "get_api_key")
        assert hasattr(config, "get_value")

    def test_filepath(self, config: GlobalConfiguration):
        assert os.path.exists(config.filepath)

    def test_configuration(self, config: GlobalConfiguration):
        assert isinstance(config._data, dict)

    def test_load_configuration(self, config: GlobalConfiguration):
        with open(config.filepath, "r") as f:
            expected_config = json.load(f)
        assert config._data == expected_config

    @pytest.mark.private
    def test_api_key(self, config: GlobalConfiguration):
        assert bool(config.get_api_key())
        assert isinstance(config.get_api_key(), str)
        assert config.get_api_key().startswith("sk-")

    def test_get_value(self, config: GlobalConfiguration):
        assert bool(config.get_value("chat_completions.model"))
        assert config.get_value("non_existent_key", "default") == "default"
        assert isinstance(config.get_value("access.shell.allowed_commands"), list)
