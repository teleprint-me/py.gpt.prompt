"""
pygptprompt/model/sequence/context.py
"""
from typing import Optional

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.database.chroma import ChromaVectorStore
from pygptprompt.model.sequence.manager import SequenceManager
from pygptprompt.model.token_manager import ContextWindowTokenManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse


# TODO: Consider making the system message optional for increased code reusability.
# This change may require restructuring the codebase and could have a ripple effect.
# Revisit this in a future sprint or version update when there's more time for planning and testing.
class ContextWindowManager(SequenceManager):
    """
    A class for managing chat model context windows.

    This class extends TranscriptManager to provide functionality for managing chat model context windows.

    Args:
        file_path (str): The file path for storing the chat context.
        provider (str): The provider of the chat model.
        config (ConfigurationManager): The configuration manager for the application.
        chat_model (ChatModel): The chat model used for generating responses.
        vector_store (Optional[ChromaVectorStore]): An optional vector store for embedding messages.
        embed (bool, optional): A flag indicating whether to embed messages in the vector store.

    Attributes:
        token_manager (ContextWindowTokenManager): The token manager for handling chat tokens.
        vector_store (Optional[ChromaVectorStore]): An optional vector store for embedding messages.
        embed (bool): A flag indicating whether to embed messages in the vector store.

    Methods:
        dequeue(): Dequeues the oldest message from the context window.
        _append_single_message(message: ChatModelResponse): Appends a single message to the context window.

    """

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
        """
        Dequeues the oldest message from the context window.

        The first element is always the system message. This method skips the system message
        in order to preserve the model's directive. It also provides logic for embedding
        messages into vectors and storing them in the vector store if embedding is enabled.

        Returns:
            None
        """
        dequeued_message = self.sequence.pop(1)
        # Embedding messages is optional and is set by the user at runtime.
        if self.vector_store is not None and self.embed:
            self.vector_store.add_message_to_collection(dequeued_message)

    def _append_single_message(self, message: ChatModelResponse) -> None:
        """
        Appends a single message to the context window.

        This method appends a single message to the context window. It checks the token size
        to determine if the message causes a chat sequence overflow and dequeues the oldest
        message if necessary.

        Args:
            message (ChatModelResponse): The message to append to the context window.

        Returns:
            None
        """
        if self.token_manager.causes_chat_sequence_overflow(message, self.sequence):
            self.dequeue()
        self.sequence.append(message)
