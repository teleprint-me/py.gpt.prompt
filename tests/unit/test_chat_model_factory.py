"""
tests/unit/test_chat_model_factory.py
"""
import pytest

from pygptprompt.api.factory import ChatModelFactory
from pygptprompt.api.llama_cpp import LlamaCppAPI
from pygptprompt.api.openai import OpenAIAPI
from pygptprompt.config.manager import ConfigurationManager


# Test cases for the ChatModelFactory
class TestChatModelFactory:
    def test_create_openai_model(self, config: ConfigurationManager):
        factory = ChatModelFactory(config)
        model = factory.create_model("openai")
        assert isinstance(model, OpenAIAPI)

    def test_create_llama_cpp_model(self, config: ConfigurationManager):
        factory = ChatModelFactory(config)
        model = factory.create_model("llama_cpp")
        assert isinstance(model, LlamaCppAPI)

    def test_unknown_provider(self, config: ConfigurationManager):
        factory = ChatModelFactory(config)
        with pytest.raises(ValueError):
            model = factory.create_model("unknown_provider")

    def test_missing_provider_config(self, config: ConfigurationManager):
        factory = ChatModelFactory(config)
        with pytest.raises(ValueError):
            model = factory.create_model("missing_provider")

    def test_missing_provider_key(self, config: ConfigurationManager):
        factory = ChatModelFactory(config)
        with pytest.raises(ValueError):
            model = factory.create_model("llama_cpp_missing_key")
