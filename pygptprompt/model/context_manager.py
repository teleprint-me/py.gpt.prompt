"""
pygptprompt/model/context_manager.py
"""
from typing import List, Optional, Union

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.database.chroma import ChromaVectorStore
from pygptprompt.model.token_manager import ContextWindowTokenManager
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModel, ChatModelResponse


class ContextWindowManager:
    def __init__(
        self,
        file_path,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
        vector_store: Optional[ChromaVectorStore] = None,
        embed: bool = False,
    ):
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
        self.vector_store = vector_store
        self.embed = embed
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

    def dequeue(self) -> None:
        # NOTE:
        # The first element is always the system message.
        # We always skip the system message in order to preserve the models directive.
        # Logic to dequeue, possibly embed into vectors and store in vector store.
        dequeued_message = self.sequence.pop(1)
        # NOTE: Embedding messages is optional and is set by user at runtime.
        if self.vector_store is not None and self.embed:
            self.vector_store.add_message_to_collection(dequeued_message)

    def append_single_message(self, message: ChatModelResponse) -> None:
        # Logic to append a single message, might want to check token size here
        if self.token_manager.causes_chat_sequence_overflow(message, self.sequence):
            self.dequeue()
        self.sequence.append(message)

    def append_multiple_messages(self, messages: List[ChatModelResponse]) -> None:
        # Logic to append multiple messages
        for message in messages:
            self.append_single_message(message)

    def enqueue(self, message: Union[ChatModelResponse, List[ChatModelResponse]]):
        # NOTE:
        # This is not polymorphic, but allows us to override the method internally.
        if isinstance(message, ChatModelResponse):
            self.append_single_message(message)
        elif isinstance(message, list):
            self.append_multiple_messages(message)
