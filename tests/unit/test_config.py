# tests/unit/test_config.py
import json
import os

import pytest

from pygptprompt.config import Configuration
from pygptprompt.singleton import Singleton


class TestConfiguration:
    def test_type(self, config: Configuration):
        assert isinstance(config, Singleton)
        assert isinstance(config, Configuration)

    def test_attributes(self, config: Configuration):
        assert hasattr(config, "filepath")
        assert hasattr(config, "data")
        assert hasattr(config, "load")
        assert hasattr(config, "get_api_key")
        assert hasattr(config, "get_value_by_key")
        assert hasattr(config, "get_value")

    def test_filepath(self, config: Configuration):
        assert os.path.exists(config.filepath)

    def test_config(self, config: Configuration):
        assert isinstance(config.data, dict)

    def test_load_configuration(self, config: Configuration):
        with open(config.filepath, "r") as f:
            expected_config = json.load(f)
        assert config.data == expected_config

    def test_get_value_by_key(self, config: Configuration):
        assert bool(config.get_value_by_key(config.data, "chat_completions"))
        assert isinstance(
            config.get_value_by_key(
                config.data,
                "allowed_commands",
            ),
            list,
        )
        assert not isinstance(
            config.get_value_by_key(
                config.data,
                "access.shell.allowed_commands",
            ),
            list,
        )
        assert isinstance(
            config.get_value_by_key(
                config.data,
                "access.file.allowed_paths",
                True,
            ),
            list,
        )

    @pytest.mark.private
    def test_api_key(self, config: Configuration):
        assert bool(config.get_api_key())
        assert isinstance(config.get_api_key(), str)
        assert config.get_api_key().startswith("sk-")

    def test_get_value(self, config: Configuration):
        assert bool(config.get_value("chat_completions"))
        assert config.get_value("non_existent_key", "default") == "default"
        assert isinstance(config.get_value("access.shell.allowed_commands"), list)
