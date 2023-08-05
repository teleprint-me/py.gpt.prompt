"""
tests/unit/session/test_token.py
"""
from typing import List

import pytest

from pygptprompt.pattern.types import ChatModelChatCompletion
from pygptprompt.session.token import ChatSessionTokenManager


class TestChatSessionTokenManager:
    def test_reserve(self, chat_session_token_manager: ChatSessionTokenManager):
        assert 0 <= chat_session_token_manager.reserve <= 1

    def test_offset(self, chat_session_token_manager: ChatSessionTokenManager):
        assert isinstance(chat_session_token_manager.offset, int)

    def test_max_length(self, chat_session_token_manager: ChatSessionTokenManager):
        assert isinstance(chat_session_token_manager.max_length, int)

    def test_max_tokens(self, chat_session_token_manager: ChatSessionTokenManager):
        assert isinstance(chat_session_token_manager.max_tokens, int)

    def test_upper_limit(self, chat_session_token_manager: ChatSessionTokenManager):
        assert isinstance(chat_session_token_manager.upper_limit, int)

    @pytest.mark.parametrize("reserve", [0.1, 0.5, 0.9])
    def test_base_limit(
        self,
        chat_session_token_manager: ChatSessionTokenManager,
        reserve: float,
    ):
        chat_session_token_manager._config.set_value(
            "llama_cpp.context.reserve", reserve
        )
        assert isinstance(chat_session_token_manager.base_limit, int)

    def test_get_sequence_length(
        self, chat_session_token_manager: ChatSessionTokenManager
    ):
        text = "This is a test text."
        length = chat_session_token_manager.get_sequence_length(text)
        assert isinstance(length, int)

    def test_get_message_length_with_fixture(
        self,
        chat_session_token_manager: ChatSessionTokenManager,
        message: ChatModelChatCompletion,
    ):
        length = chat_session_token_manager.get_message_length(message)
        assert isinstance(length, int)

    def test_get_total_message_length_with_fixture(
        self,
        chat_session_token_manager: ChatSessionTokenManager,
        messages: List[ChatModelChatCompletion],
    ):
        total_length = chat_session_token_manager.get_total_message_length(messages)
        assert isinstance(total_length, int)

    def test_is_overflow_with_fixture(
        self,
        chat_session_token_manager: ChatSessionTokenManager,
        message: ChatModelChatCompletion,
        messages: List[ChatModelChatCompletion],
    ):
        overflow = chat_session_token_manager.is_overflow(message, messages)
        assert isinstance(overflow, bool)
