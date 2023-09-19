"""
pygptprompt/model/context_manager.py
"""
from typing import List, Union

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.model.token_manager import ContextWindowTokenManager
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModelResponse


class ContextWindowManager:
    def __init__(self, file_path, provider: str, config: ConfigurationManager):
        model_factory = ChatModelFactory(config=config)
        chat_model = model_factory.create_model(provider=provider)
        self.config = config
        self.logger = config.get_logger(
            key="app.log.general",
            logger_name="ContextWindowManager",
            level="DEBUG",
        )
        self.list_template = ListTemplate(file_path=file_path, logger=self.logger)
        self.token_manager = ContextWindowTokenManager(
            provider=provider, config=config, chat_model=chat_model
        )

    def load_to_chat_completions(self) -> bool:
        """
        Load JSON data from the file into the _data attribute.

        Returns:
            bool: True if the JSON data was loaded successfully, False on error.
        """
        if self.load_json():
            self.sequence = [
                ChatModelResponse(**message) for message in self.list_template.data
            ]
            return True
        return False

    def save_from_chat_completions(self) -> bool:
        """
        Save the _data attribute to the JSON file.

        Returns:
            bool: True if the JSON data was saved successfully, False on error.
        """
        if self._data:
            data = [dict(message) for message in self.sequence]
            # NOTE: list_template._data is internally updated once we write to disk
            return self.list_template.save_json(data)
        return False

    def enqueue(self, message: Union[ChatModelResponse, List[ChatModelResponse]]):
        if isinstance(message, ChatModelResponse):
            # Handle single ChatModelResponse
            self.append_single_message(message)
        elif isinstance(message, list):
            # Handle list of ChatModelResponses
            self.append_multiple_messages(message)

    def dequeue(self):
        ...
