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

    def test_reserve_in_range(self, token_manager: ChatSessionTokenManager):
        """
        Test that the reserve is within the valid range [0, 1].
        """
        assert 0 <= token_manager.reserve <= 1

    def test_offset(self, token_manager: ChatSessionTokenManager):
        """
        Test that the token offset is set and valid.
        """
        assert isinstance(token_manager.offset, int)

    def test_max_sequence(self, token_manager: ChatSessionTokenManager):
        """
        Test that the maximum number of tokens is set and valid.
        """
        assert isinstance(token_manager.max_sequence, int)

    def test_max_tokens(self, token_manager: ChatSessionTokenManager):
        """
        Test that the maximum sequence length is set and valid.
        """
        assert isinstance(token_manager.max_tokens, int)

    def test_calculate_upper_bound(self, token_manager: ChatSessionTokenManager):
        """
        Test the calculation of the upper bound for the model's output.
        """
        assert isinstance(token_manager.upper_bound, int)

    @pytest.mark.parametrize("reserve", [0.1, 0.5, 0.9])
    def test_calculate_reserved_upper_bound(
        self, token_manager: ChatSessionTokenManager, reserve: float
    ):
        """
        Test calculating the reserved upper bound value for content size management.
        """
        token_manager._config.set_value("llama_cpp.context.reserve", reserve)
        assert isinstance(token_manager.reserve, float)

    def test_calculate_sequence_length(self, token_manager: ChatSessionTokenManager):
        """
        Test the calculation of token sequence length from a text input.
        """
        text = "This is a test text."
        length = token_manager.calculate_text_sequence_length(text)
        assert isinstance(length, int)

    def test_calculate_message_length_with_fixture(
        self, token_manager: ChatSessionTokenManager, message: ChatModelResponse
    ):
        """
        Test the calculation of token message length using a fixture.
        """
        length = token_manager.calculate_chat_message_length(message)
        assert isinstance(length, int)

    def test_calculate_total_sequence_length_with_fixture(
        self, token_manager: ChatSessionTokenManager, messages: List[ChatModelResponse]
    ):
        """
        Test the calculation of total token sequence length using a fixture.
        """
        total_length = token_manager.calculate_chat_sequence_length(messages)
        assert isinstance(total_length, int)

    def test_causes_sequence_overflow_with_fixture(
        self,
        token_manager: ChatSessionTokenManager,
        message: ChatModelResponse,
        messages: List[ChatModelResponse],
    ):
        """
        Test if adding a new message causes a sequence overflow using a fixture.
        """
        overflow = token_manager.causes_chat_sequence_overflow(message, messages)
        assert isinstance(overflow, bool)
