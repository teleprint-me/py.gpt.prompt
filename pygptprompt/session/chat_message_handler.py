"""
pygptprompt/session/token.py
"""
from typing import List, Literal

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.model import ChatModel
from pygptprompt.pattern.types import ChatModelChatCompletion


class ChatMessageHandler:
    """
    A helper class for managing individual chat messages within a chat session.

    Args:
        provider (str): The provider or source of the chat session.
        config (ConfigurationManager): The configuration manager for chat settings.
        model (ChatModel): The chat model used for processing messages.
    """

    def __init__(
        self,
        provider: str,
        config: ConfigurationManager,
        model: ChatModel,
    ):
        """
        Initializes the ChatMessageHandler.

        Args:
            provider (str): The provider or source of the chat session.
            config (ConfigurationManager): The configuration manager for chat settings.
            model (ChatModel): The chat model used for processing messages.
        """
        self._provider = provider
        self._config = config
        self._model = model

    @property
    def reserve(self) -> float:
        """A floating-point value between 0 and 1 that represents a percentage of the maximum sequence length for the given model."""
        return self._config.get_value(f"{self._provider}.context.reserve")

    @property
    def offset(self) -> int:
        """The number of tokens to offset within a given sequence."""
        return self._config.get_value(f"{self._provider}.context.offset")

    @property
    def max_length(self) -> int:
        """An integer value representing the maximum sequence length for the given model."""
        return self._config.get_value(f"{self._provider}.context.length")

    @property
    def max_tokens(self) -> int:
        """An integer value representing the maximum sequence length the model is allowed to generate."""
        return self._config.get_value(f"{self._provider}.chat_completions.max_tokens")

    @property
    def upper_limit(self) -> int:
        """Get the token limit for the model from the dictionary, or use the default limit."""
        return self.max_length - self.max_tokens

    @property
    def base_limit(self) -> int:
        """Calculate the base limit as a percentage of the upper limit."""
        return int(self.upper_limit * self.reserve)

    def get_sequence_length(self, text: str) -> int:
        """Count the number of tokens within the given text sequence."""
        return len(self._model.get_encoding(text=text))

    def get_message_length(self, message: ChatModelChatCompletion) -> int:
        """
        Returns the number of tokens in a given message.

        Args:
            message (ChatModelChatCompletion): The message to process.

        Returns:
            int: The number of tokens in the message.
        """
        sequence: str = ""

        for key, value in message.items():
            if value is not None:
                sequence += " " + key + " " + value

        return self.get_sequence_length(sequence.strip())

    def get_total_message_length(
        self,
        messages: List[ChatModelChatCompletion],
    ) -> int:
        """
        Returns the total number of tokens in a list of chat messages.

        Args:
            messages (List[ChatModelChatCompletion]): The list of messages.

        Returns:
            int: The total number of tokens in the list of messages.
        """
        total_tokens: int = 0

        for message in messages:
            total_tokens += self.get_message_length(message)

        return total_tokens

    def is_overflow(
        self,
        new_message: ChatModelChatCompletion,
        messages: List[ChatModelChatCompletion],
    ) -> bool:
        """
        Check if adding a new message will cause the sequence to overflow.

        Args:
            new_message (ChatModelChatCompletion): The new message to be added.
            messages (List[ChatModelChatCompletion]): The existing list of messages.

        Returns:
            bool: True if the sequence will overflow, False otherwise.
        """
        new_message_token_count = self.get_message_length(new_message)
        messages_total_token_count = self.get_total_message_length(messages)
        token_count = new_message_token_count + messages_total_token_count
        total_token_count = self.offset + token_count
        return total_token_count >= self.upper_limit
