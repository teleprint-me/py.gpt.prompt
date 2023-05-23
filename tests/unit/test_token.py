# tests/unit/test_token.py
from tiktoken import Encoding

from pygptprompt.chat.token import ChatToken


class TestChatToken:
    def test_attributes(self, chat_token: ChatToken):
        assert hasattr(chat_token, "model")
        assert hasattr(chat_token, "max_tokens")
        assert hasattr(chat_token, "encoding")
        assert hasattr(chat_token, "upper_limit")
        assert hasattr(chat_token, "is_message_within_limit")
        assert hasattr(chat_token, "get_token_count")
        assert hasattr(chat_token, "enqueue")
        assert hasattr(chat_token, "dequeue")

    def test_types(self, chat_token: ChatToken):
        assert isinstance(chat_token, ChatToken)
        assert isinstance(chat_token.model, str)
        assert isinstance(chat_token.max_tokens, int)
        assert isinstance(chat_token.encoding, Encoding)
        assert isinstance(chat_token.upper_limit, int)

    def test_limits(
        self,
        chat_token: ChatToken,
        messages: list[dict[str, str]],
    ):
        chat_token.model = "gpt-3.5-turbo"
        assert chat_token.upper_limit == 4096 - chat_token.max_tokens

        chat_token.model = "gpt-4"
        assert chat_token.upper_limit == 8192 - chat_token.max_tokens

        chat_token.model = "davinci"
        assert chat_token.upper_limit == 2048 - chat_token.max_tokens

        token_count = chat_token.get_token_count(messages)
        assert chat_token.is_message_within_limit(token_count)

    def test_get_token_count(
        self,
        chat_token: ChatToken,
        messages: list[dict[str, str]],
    ):
        assert chat_token.get_token_count(messages) == 29

    def test_enqueue(
        self,
        chat_token: ChatToken,
        messages: list[dict[str, str]],
    ):
        new_message = {"role": "user", "content": "This is a new message."}
        updated_messages = chat_token.enqueue(messages, new_message)

        # Check that the new message was added to the list
        assert updated_messages[-1] == new_message

        # Check that the total token count is within the limit
        total_token_count = chat_token.get_token_count(updated_messages)
        assert total_token_count <= chat_token.upper_limit

    def test_dequeue(
        self,
        chat_token: ChatToken,
        messages: list[dict[str, str]],
    ):
        # Add a new message to make the total token count exceed the limit
        new_message = {"role": "user", "content": "This is a very long message." * 100}
        messages.append(new_message)

        updated_messages = chat_token.dequeue(
            messages, chat_token.get_token_count([new_message])
        )

        # Ensure system message is preserved
        assert updated_messages[0]["role"] == messages[0]["role"]
        assert updated_messages[0]["content"] == messages[0]["content"]

        # Check that the total token count is within the limit
        total_token_count = chat_token.get_token_count(updated_messages)
        assert total_token_count <= chat_token.upper_limit
