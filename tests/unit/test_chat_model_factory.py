"""
tests/unit/test_chat_model_factory.py
"""
import pytest

from pygptprompt.api.factory import ChatModelFactory
from pygptprompt.api.llama_cpp import LlamaCppAPI
from pygptprompt.api.openai import OpenAIAPI


class TestChatModelFactory:
    def test_create_openai_model(self, chat_model_factory: ChatModelFactory):
        model = chat_model_factory.create_model("openai")
        assert isinstance(model, OpenAIAPI)

    def test_create_llama_cpp_model(self, chat_model_factory: ChatModelFactory):
        model = chat_model_factory.create_model("llama_cpp")
        assert isinstance(model, LlamaCppAPI)

    def test_unknown_provider(self, chat_model_factory: ChatModelFactory):
        with pytest.raises(ValueError):
            model = chat_model_factory.create_model("unknown_provider")

    def test_missing_provider_config(self, chat_model_factory: ChatModelFactory):
        with pytest.raises(ValueError):
            model = chat_model_factory.create_model("missing_provider")

    def test_missing_provider_key(self, chat_model_factory: ChatModelFactory):
        with pytest.raises(ValueError):
            model = chat_model_factory.create_model("llama_cpp_missing_key")
