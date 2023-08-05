"""
"There are only two hard things in Computer Science: cache invalidation and naming things."
    - Phil Karlton

pygptprompt/session/token.py
"""
from typing import List

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.model import ChatModel
from pygptprompt.pattern.types import ChatModelChatCompletion


class ChatSessionTokenManager:
    """
    A helper class for managing tokens within a chat session.

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
        Initializes the ChatSessionTokenManager.

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
        """
        A floating-point value between 0 and 1 that represents the percentage of the maximum
        sequence length reserved for special content injection during a chat session.

        The reserve ensures that there is sufficient space in the context window to accommodate
        special content injected into the sequence without disrupting the ongoing chat session.

        If the injected content exceeds the reserve, as much of it as possible will be put
        into the sequence, or an appropriate notice will be provided if it can't fit within
        the reserved space.

        Returns:
            float: The percentage of the maximum sequence length reserved for special content injection.
        """
        return self._config.get_value(f"{self._provider}.context.reserve", default=0.1)

    @property
    def offset(self) -> int:
        """
        The number of tokens to offset within a given sequence.

        The offset value acts as padding for the sequence, ensuring that there is a safe buffer space
        within the context window and preventing accidental sequence overflows. Using the offset
        helps maintain the stability and robustness of the chat session.

        Returns:
            int: The number of tokens to offset within a given sequence.
        """
        return self._config.get_value(f"{self._provider}.context.offset", default=256)

    @property
    def max_length(self) -> int:
        """
        An integer value representing the maximum sequence length for the given model.

        The max_length property defines the maximum number of tokens the model can handle
        at any given moment in time, representing its context window size.

        Returns:
            int: The maximum sequence length for the given model.
        """
        return self._config.get_value(f"{self._provider}.context.length", default=2048)

    @property
    def max_tokens(self) -> int:
        """
        An integer value representing the maximum sequence length the model is allowed to generate.

        The max_tokens property defines the maximum number of tokens the model can generate
        as its output, considering the given input sequence.

        Returns:
            int: The maximum sequence length the model is allowed to generate.
        """
        return self._config.get_value(
            f"{self._provider}.chat_completions.max_tokens", default=512
        )

    @property
    def upper_limit(self) -> int:
        """
        The artificial ceiling that guarantees the model's output fits within the defined sequence length.

        The upper_limit property calculates the maximum token limit for the model, ensuring that the model's
        output always fits within the given sequence length. It achieves this by subtracting the maximum
        number of tokens the model is allowed to generate (max_tokens) from the maximum sequence length
        for the given model (max_length).

        Returns:
            int: The token limit representing the artificial ceiling for the model's output length.
        """
        return self.max_length - self.max_tokens

    @property
    def base_limit(self) -> int:
        """
        Calculate the base limit as a percentage of the upper limit for content size management.

        The base_limit property calculates a limit that ensures the model's output, considering
        the reserved space (based on the reserve property), remains within a certain proportion
        of the artificial ceiling (upper_limit) that guarantees the model's output fits within
        the defined sequence length. This calculated limit serves as a threshold for managing the
        size of content displayed within the chat session.

        Returns:
            int: The calculated base limit as a percentage of the upper limit.
        """
        return int(self.upper_limit * self.reserve)

    def get_sequence_length(self, text: str) -> int:
        """
        Count the number of tokens within the given text sequence.

        Args:
            text (str): The input text sequence.

        Returns:
            int: The number of tokens in the input text sequence after tokenization.
        """
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
