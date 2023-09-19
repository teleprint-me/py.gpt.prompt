"""
pygptprompt/model/transcript_manager.py
"""
from typing import List, Union

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModelResponse


class TranscriptManager:
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

    def load_to_chat_completions(self) -> bool:
        if self.list_template.load_json():
            self.sequence = [
                ChatModelResponse(**message) for message in self.list_template.data
            ]
            return True
        return False

    def save_from_chat_completions(self) -> bool:
        if self.sequence:
            data: List[ChatModelResponse] = [dict(message) for message in self.sequence]
            return self.list_template.save_json(data)
        return False

    def _append_single_message(self, message: ChatModelResponse) -> None:
        self.sequence.append(message)

    def _append_multiple_messages(self, messages: List[ChatModelResponse]) -> None:
        # Logic to append multiple messages
        for message in messages:
            self.append_single_message(message)

    def enqueue(self, message: Union[ChatModelResponse, List[ChatModelResponse]]):
        # NOTE:
        # This is not polymorphic, but allows us to override the method internally.
        if isinstance(message, ChatModelResponse):
            self._append_single_message(message)
        elif isinstance(message, list):
            self._append_multiple_messages(message)
