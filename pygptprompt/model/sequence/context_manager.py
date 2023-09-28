"""
pygptprompt/model/sequence/context.py
"""
from typing import Optional

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.sequence.sequence_manager import SequenceManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse
from pygptprompt.storage.chroma import ChromaVectorStore


# TODO: Consider making the system message optional for increased code reusability.
# This change may require restructuring the codebase and could have a ripple effect.
# Revisit this in a future sprint or version update when there's more time for planning and testing.
class ContextWindowManager(SequenceManager):
    """
    A class for managing chat model context windows.

    This class extends TranscriptManager to provide functionality for managing chat model context windows.

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
        vector_store: Optional[ChromaVectorStore] = None,
    ):
        super().__init__(file_path, provider, config, chat_model)

        self.vector_store = vector_store

    @property
    def reserved_upper_bound(self) -> int:
        """
        Get the reserved upper bound for the sequence length.

        This property defines the maximum number of tokens reserved for content injection,
        such as responses from documents or web requests.

        Returns:
            int: The reserved upper bound for the sequence length.
        """
        return self.token_manager.reserved_upper_bound

    def dequeue(self) -> ChatModelResponse:
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
        if self.vector_store is not None:
            self.vector_store.add_message_to_collection(dequeued_message)

        return dequeued_message

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
