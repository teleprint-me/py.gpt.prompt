"""
pygptprompt/model/sequence/manager.py
"""

from typing import Iterator, List, Protocol, Union

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModelResponse


class SequenceManager(Protocol):
    """
    Interface for managing sequences of ChatModelResponse objects.

    This abstract class defines methods and properties for managing sequences
    of ChatModelResponse objects, including loading and saving from JSON, appending,
    dequeuing, and other common sequence operations.

    Args:
        file_path (str): The file path to the JSON data storage.
        config (ConfigurationManager): The configuration manager for logging.

    Attributes:
        logger (Logger): The logger instance for logging messages.
        list_template (ListTemplate): The template for working with JSON lists.
        sequence (List[ChatModelResponse]): The list of ChatModelResponse objects.

    Properties:
        system_message (ChatModelResponse): The system message at the beginning of the sequence.

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
        config: ConfigurationManager,
    ):
        self.logger = config.get_logger(
            key="app.log.general",
            logger_name=self.__class__.__name__,
            level="DEBUG",
        )
        self.list_template = ListTemplate(file_path=file_path, logger=self.logger)
        self.sequence = []

    def __len__(self) -> int:
        """Get the length of the sequence."""
        return len(self.sequence)

    def __getitem__(self, index) -> ChatModelResponse:
        """Get a ChatModelResponse at the specified index."""
        return self.sequence[index]

    def __setitem__(self, index: int, value: ChatModelResponse):
        """Set a ChatModelResponse at the specified index."""
        self.sequence[index] = value

    def __delitem__(self, index: int):
        """Delete a ChatModelResponse at the specified index."""
        del self.sequence[index]

    def __iter__(self) -> Iterator[ChatModelResponse]:
        """Get an iterator for the sequence."""
        return iter(self.sequence)

    def __contains__(self, item: ChatModelResponse):
        """Check if a ChatModelResponse is in the sequence."""
        return item in self.sequence

    @property
    def system_message(self) -> ChatModelResponse:
        """
        Get the system message at the beginning of the sequence.

        Returns:
            ChatModelResponse: The system message.
        """
        try:
            return self.sequence[0]
        except IndexError:
            return ChatModelResponse(role="", content="")

    def load_to_chat_completions(self) -> bool:
        """
        Load data from JSON into the sequence.

        Returns:
            bool: True if loading was successful, False on error.
        """
        if self.list_template.load_json():
            self.sequence = [
                ChatModelResponse(**message) for message in self.list_template.data
            ]
            return True
        return False

    def save_from_chat_completions(self) -> bool:
        """
        Save the sequence to JSON.

        Returns:
            bool: True if saving was successful, False on error.
        """
        if self.sequence:
            data: List[ChatModelResponse] = [dict(message) for message in self.sequence]
            return self.list_template.save_json(data)
        return False

    def _append_single_message(self, message: ChatModelResponse) -> None:
        """
        Append a single ChatModelResponse to the sequence.

        Args:
            message (ChatModelResponse): The ChatModelResponse to append.
        """
        self.sequence.append(message)

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
        if isinstance(message, ChatModelResponse):
            self._append_single_message(message)
        elif isinstance(message, list):
            self._append_multiple_messages(message)
