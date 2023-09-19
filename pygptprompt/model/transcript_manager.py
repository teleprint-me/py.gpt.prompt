"""
pygptprompt/model/transcript_manager.py
"""
from typing import List, Union

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModelResponse


class TranscriptManager:
    """
    A class for managing transcripts of chat completions.

    This class provides methods for loading and saving chat completion data to/from JSON files.

    Attributes:
        logger (Logger): The logger for recording log messages.
        list_template (ListTemplate): The template for managing the list data structure.
        sequence (List[ChatModelResponse]): The list of chat completion messages.

    Args:
        file_path (str): The file path to the JSON file used to store chat completion data.
        config (ConfigurationManager): The configuration manager for accessing settings and configurations.
    """

    def __init__(
        self,
        file_path: str,
        config: ConfigurationManager,
    ):
        """
        Initializes a new TranscriptManager instance.

        Args:
            file_path (str): The file path to the JSON file used to store chat completion data.
            config (ConfigurationManager): The configuration manager for accessing settings and configurations.
        """
        self.logger = config.get_logger(
            key="app.log.general",
            logger_name=self.__class__.__name__,
            level="DEBUG",
        )
        self.list_template = ListTemplate(file_path=file_path, logger=self.logger)
        self.sequence = []

    def load_to_chat_completions(self) -> bool:
        """
        Load chat completion data from a JSON file into the sequence.

        Returns:
            bool: True if the data was loaded successfully, False on error.
        """
        if self.list_template.load_json():
            self.sequence = [
                ChatModelResponse(**message) for message in self.list_template.data
            ]
            return True
        return False

    def save_from_chat_completions(self) -> bool:
        """
        Save chat completion data from the sequence to a JSON file.

        Returns:
            bool: True if the data was saved successfully, False on error.
        """
        if self.sequence:
            data: List[ChatModelResponse] = [dict(message) for message in self.sequence]
            return self.list_template.save_json(data)
        return False

    def _append_single_message(self, message: ChatModelResponse) -> None:
        """
        Append a single chat completion message to the sequence.

        Args:
            message (ChatModelResponse): The chat completion message to append.
        """
        self.sequence.append(message)

    def _append_multiple_messages(self, messages: List[ChatModelResponse]) -> None:
        """
        Append multiple chat completion messages to the sequence.

        Args:
            messages (List[ChatModelResponse]): The list of chat completion messages to append.
        """
        for message in messages:
            self.append_single_message(message)

    def enqueue(self, message: Union[ChatModelResponse, List[ChatModelResponse]]):
        """
        Enqueue a chat completion message or a list of messages into the sequence.

        Args:
            message (Union[ChatModelResponse, List[ChatModelResponse]]): The chat completion message(s) to enqueue.
        """
        if isinstance(message, ChatModelResponse):
            self._append_single_message(message)
        elif isinstance(message, list):
            self._append_multiple_messages(message)
