# tests/unit/test_token.py
from tiktoken import Encoding

from pygptprompt.session.token import SessionToken


class TestChatToken:
    def test_attributes(self, session_token: SessionToken):
        assert hasattr(session_token, "model")
        assert hasattr(session_token, "max_tokens")
        assert hasattr(session_token, "encoding")
        assert hasattr(session_token, "upper_limit")
        assert hasattr(session_token, "get_count")
        assert hasattr(session_token, "get_total_count")
        assert hasattr(session_token, "is_overflow")

    def test_types(self, session_token: SessionToken):
        assert isinstance(session_token, SessionToken)
        assert isinstance(session_token.model, str)
        assert isinstance(session_token.max_tokens, int)
        assert isinstance(session_token.encoding, Encoding)
        assert isinstance(session_token.upper_limit, int)

    def test_limits(
        self,
        session_token: SessionToken,
        message: dict[str, str],
        messages: list[dict[str, str]],
    ):
        session_token.model = "gpt-3.5-turbo"
        assert session_token.upper_limit == 4096 - session_token.max_tokens

        session_token.model = "gpt-4"
        assert session_token.upper_limit == 8192 - session_token.max_tokens

        session_token.model = "davinci"
        assert session_token.upper_limit == 2048 - session_token.max_tokens

        assert not session_token.is_overflow(message, messages)

    def test_get_count(
        self,
        session_token: SessionToken,
        message: dict[str, str],
    ):
        assert session_token.get_count(message) == 17

    def test_get_total_count(
        self,
        session_token: SessionToken,
        messages: list[dict[str, str]],
    ):
        assert session_token.get_total_count(messages) == 29
