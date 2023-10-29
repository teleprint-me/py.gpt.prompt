"""
tests/unit/config/test_manager.py
"""
import os

import pytest

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.json.mapping import JSONMappingTemplate
from pygptprompt.pattern.singleton import Singleton


class TestConfigurationManager:
    def test_types(self, config: ConfigurationManager):
        assert isinstance(config, Singleton)
        assert isinstance(config, ConfigurationManager)

    def test_attributes(self, config: ConfigurationManager):
        assert hasattr(config, "load")
        assert hasattr(config, "save")
        assert hasattr(config, "backup")
        assert hasattr(config, "get_value")
        assert hasattr(config, "set_value")
        assert hasattr(config, "evaluate_path")
        assert hasattr(config, "get_environment")

    def test_mapping(self, config: ConfigurationManager):
        assert hasattr(config, "_map_template")
        assert isinstance(config._map_template, JSONMappingTemplate)

    def test_configuration(self, config: ConfigurationManager):
        assert os.path.exists(config._map_template.file_path)
        assert isinstance(config._map_template.data, dict)

    def test_get_value(self, config: ConfigurationManager):
        assert bool(config.get_value("openai.chat_completions.model")) is True
        assert config.get_value("non_existent_key", "default") == "default"
        assert isinstance(config.get_value("app.access.shell.allowed_commands"), list)

    def test_evaluate_path_app_path_test(self, config: ConfigurationManager):
        path = config.evaluate_path("app.test", "tests/tmp")
        assert path == "tests/tmp"

    def test_evaluate_path_app_path_local(
        self, config: ConfigurationManager, monkeypatch
    ):
        # Simulate the HOME environment variable
        monkeypatch.setenv("HOME", "/home/testuser")

        path = config.evaluate_path("app.local", "tests/tmp")
        assert path == "local"

    @pytest.mark.private
    def test_openai_api_key(self, config: ConfigurationManager):
        assert bool(config.get_environment()) is True
        assert isinstance(config.get_environment(), str)
        assert config.get_environment().startswith("sk-")
