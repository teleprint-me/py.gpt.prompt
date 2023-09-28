"""
pygptprompt/model/sequence/manager.py
"""

from typing import Iterator, List, Protocol, Union

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.sequence.token_manager import TokenManager
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModel, ChatModelResponse


class SequenceManager(Protocol):
    """
    Interface for managing sequences of ChatModelResponse objects.

    This abstract class defines methods and properties for managing sequences
    of ChatModelResponse objects, including loading and saving from JSON, appending,
    dequeuing, and other common sequence operations.

    Args:
        file_path (str): The file path to the JSON file used to store chat completion data.
        provider (str): The provider or source of chat completions.
        config (ConfigurationManager): The configuration manager for accessing settings and configurations.
        chat_model (ChatModel): The chat model used for managing chat completions.

    Attributes:
        logger (Logger): The logger instance for logging messages.
        list_template (ListTemplate): The template for working with JSON lists.
        token_manager (ContextWindowTokenManager): The token manager for handling chat tokens.
        sequence (List[ChatModelResponse]): The list of ChatModelResponse objects.

    Properties:
        system_message (ChatModelResponse): The system message at the beginning of the sequence.
        token_count (int): The total count of tokens in the sequence.
        reserved_upper_bound (int): Get the reserved upper bound for the sequence length.

    Methods:
        __len__(): Get the length of the sequence.
        __getitem__(index): Get a ChatModelResponse at the specified index.
        __setitem__(index, value): Set a ChatModelResponse at the specified index.
        __delitem__(index): Delete a ChatModelResponse at the specified index.
        __iter__(): Get an iterator for the sequence.
        __contains__(item): Check if a ChatModelResponse is in the sequence.
        load_to_chat_completions(): Load data from JSON into the sequence.
        save_from_chat_completions(): Save the sequence to JSON.
        _append_single_message(message): Append a single ChatModelResponse to the sequence.
        _append_multiple_messages(messages): Append multiple ChatModelResponse objects to the sequence.
        enqueue(message): Add a ChatModelResponse or a list of them to the sequence.
    """

    def __init__(
        self,
        file_path: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        self.logger = config.get_logger(
            key="app.log.general",
            logger_name=self.__class__.__name__,
            level="DEBUG",
        )

        self._sequence = []

        self._token_manager = TokenManager(
            provider=provider, config=config, chat_model=chat_model
        )

        self._list_template = ListTemplate(file_path=file_path, logger=self.logger)

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self._sequence)

    def __getitem__(self, index) -> ChatModelResponse:
        """Get a ChatModelResponse at the specified index."""
        return self._sequence[index]

    def __setitem__(self, index: int, value: ChatModelResponse):
        """Set a ChatModelResponse at the specified index."""
        self._sequence[index] = value

    def __delitem__(self, index: int):
        """Delete a ChatModelResponse at the specified index."""
        del self._sequence[index]

    def __iter__(self) -> Iterator[ChatModelResponse]:
        """Get an iterator for the sequence."""
        return iter(self._sequence)

    def __contains__(self, item: ChatModelResponse):
        """Check if a ChatModelResponse is in the sequence."""
        return item in self._sequence

    @property
    def sequence(self) -> List[ChatModelResponse]:
        """
        Get the sequence of ChatModelResponse objects.

        Returns:
            List[ChatModelResponse]: The sequence of chat responses.

        NOTE:
            A sequence is expected to only ever contain a single system message, and the system message should be the first element. Any other form is considered undefined behavior.
        """
        return self._sequence

    @property
    def token_manager(self) -> TokenManager:
        """
        Get the token manager for handling chat tokens.

        Returns:
            TokenManager: The token manager instance.
        """
        return self._token_manager

    @property
    def token_count(self) -> int:
        """
        Get the total count of tokens in the sequence.

        Returns:
            int: The total number of tokens.
        """
        return self._token_manager.calculate_chat_sequence_length(self._sequence)

    @property
    def system_message(self) -> ChatModelResponse:
        """
        Get the system message at the beginning of the sequence.

        Returns:
            ChatModelResponse: The system message, or an empty message if no system prompt is found.
        """
        if self._sequence and self._sequence[0]["role"] == "system":
            return self._sequence[0]

        # If no system prompt is found, return an empty message
        return ChatModelResponse(role="", content="")

    @system_message.setter
    def system_message(self, value: ChatModelResponse) -> None:
        """
        Set or modify the system message.

        Args:
            value (ChatModelResponse): The new system message.
        """
        if len(self._sequence) > 0:
            # Check the role of the first message
            if self._sequence[0]["role"] == "system":
                # Replace the existing system message
                self._sequence[0] = value
            else:
                # Insert a new system message at the beginning
                self._sequence.insert(0, value)
        else:
            # If the sequence is empty, add the system message
            self._sequence.append(value)

    def load_to_chat_completions(self) -> bool:
        """
        Load data from JSON into the sequence.

        Returns:
            bool: True if loading was successful, False on error.
        """
        if self._list_template.load_json():
            self._sequence = [
                ChatModelResponse(**message) for message in self._list_template.data
            ]
            return True
        return False

    def save_from_chat_completions(self) -> bool:
        """
        Save the sequence to JSON.

        Returns:
            bool: True if saving was successful, False on error.
        """
        if self._sequence:
            data: List[ChatModelResponse] = [
                dict(message) for message in self._sequence
            ]
            return self._list_template.save_json(data)
        return False

    def _append_single_message(self, message: ChatModelResponse) -> None:
        """
        Append a single ChatModelResponse to the sequence.

        Args:
            message (ChatModelResponse): The ChatModelResponse to append.
        """
        self._sequence.append(message)

    def _append_multiple_messages(self, messages: List[ChatModelResponse]) -> None:
        """
        Append multiple ChatModelResponse objects to the sequence.

        Args:
            messages (List[ChatModelResponse]): The list of ChatModelResponse objects to append.
        """
        for message in messages:
            self.append_single_message(message)

    def enqueue(
        self, message: Union[ChatModelResponse, List[ChatModelResponse]]
    ) -> None:
        """
        Add a ChatModelResponse or a list of them to the sequence.

        Args:
            message (Union[ChatModelResponse, List[ChatModelResponse]]): The ChatModelResponse or list of them to add.
        """
        if isinstance(message, list):
            self._append_multiple_messages(message)
        else:  # TypedDict does not support instance and class checks
            self._append_single_message(message)
