"""
tests/unit/session/test_token.py
"""
from typing import List

import pytest

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse
from pygptprompt.session.token import ChatSessionTokenManager


class TestChatSessionTokenManager:
    def test_attributes(self, token_manager: ChatSessionTokenManager):
        assert hasattr(token_manager, "_provider")
        assert hasattr(token_manager, "_config")
        assert hasattr(token_manager, "_model")
        assert isinstance(token_manager._provider, str)
        assert isinstance(token_manager._config, ConfigurationManager)
        assert isinstance(token_manager._model, ChatModel)

    def test_reserve_range(self, token_manager: ChatSessionTokenManager):
        assert 0 <= token_manager.reserve <= 1

    def test_offset(self, token_manager: ChatSessionTokenManager):
        assert isinstance(token_manager.offset, int)

    def test_max_length(self, token_manager: ChatSessionTokenManager):
        assert isinstance(token_manager.max_length, int)

    def test_max_tokens(self, token_manager: ChatSessionTokenManager):
        assert isinstance(token_manager.max_tokens, int)

    def test_upper_bound(self, token_manager: ChatSessionTokenManager):
        assert isinstance(token_manager.upper_bound, int)

    @pytest.mark.parametrize("reserve", [0.1, 0.5, 0.9])
    def test_reserve_setting(
        self,
        token_manager: ChatSessionTokenManager,
        reserve: float,
    ):
        token_manager._config.set_value("llama_cpp.context.reserve", reserve)
        assert isinstance(token_manager.reserve, float)

    def test_get_sequence_length(self, token_manager: ChatSessionTokenManager):
        text = "This is a test text."
        length = token_manager.get_sequence_length(text)
        assert isinstance(length, int)

    def test_get_message_length_with_fixture(
        self,
        token_manager: ChatSessionTokenManager,
        message: ChatModelResponse,
    ):
        length = token_manager.get_message_length(message)
        assert isinstance(length, int)

    def test_get_total_message_length_with_fixture(
        self,
        token_manager: ChatSessionTokenManager,
        messages: List[ChatModelResponse],
    ):
        total_length = token_manager.get_total_message_length(messages)
        assert isinstance(total_length, int)

    def test_is_overflow_with_fixture(
        self,
        token_manager: ChatSessionTokenManager,
        message: ChatModelResponse,
        messages: List[ChatModelResponse],
    ):
        overflow = token_manager.is_overflow(message, messages)
        assert isinstance(overflow, bool)
        assert isinstance(overflow, bool)
