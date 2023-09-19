"""
pygptprompt/model/context_manager.py
"""
from typing import Optional

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.database.chroma import ChromaVectorStore
from pygptprompt.model.token_manager import ContextWindowTokenManager
from pygptprompt.model.transcript_manager import TranscriptManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse


# TODO: Consider making the system message optional for increased code reusability.
# This change may require restructuring the codebase and could have a ripple effect.
# Revisit this in a future sprint or version update when there's more time for planning and testing.
class ContextWindowManager(TranscriptManager):
    def __init__(
        self,
        file_path: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
        vector_store: Optional[ChromaVectorStore] = None,
        embed: bool = False,
    ):
        super().__init__(file_path, config)

        self.token_manager = ContextWindowTokenManager(
            provider=provider, config=config, chat_model=chat_model
        )

        self.vector_store = vector_store
        self.embed = embed

    def dequeue(self) -> None:
        # NOTE:
        # The first element is always the system message.
        # We always skip the system message in order to preserve the models directive.
        # Logic to dequeue, possibly embed into vectors and store in vector store.
        dequeued_message = self.sequence.pop(1)
        # NOTE: Embedding messages is optional and is set by user at runtime.
        if self.vector_store is not None and self.embed:
            self.vector_store.add_message_to_collection(dequeued_message)

    def _append_single_message(self, message: ChatModelResponse) -> None:
        # NOTE: We have to override this method from the parent class
        # Logic to append a single message, might want to check token size here
        if self.token_manager.causes_chat_sequence_overflow(message, self.sequence):
            self.dequeue()
        self.sequence.append(message)
