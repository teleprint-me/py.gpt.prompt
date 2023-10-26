"""
pygptprompt/model/sequence/transcript.py
"""
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import ChatModel
from pygptprompt.model.sequence.sequence_manager import SequenceManager


class TranscriptManager(SequenceManager):
    """
    A class for managing transcripts of chat completions.

    This class provides methods for loading and saving chat completion data to/from JSON files.

    Args:
        file_path (str): The file path to the JSON file used to store chat completion data.
        provider (str): The provider or source of chat completions.
        config (ConfigurationManager): The configuration manager for accessing settings and configurations.
        chat_model (ChatModel): The chat model used for managing chat completions.

    Attributes:
        logger (Logger): The logger instance for logging messages.
        list_template (JSONListTemplate): The template for working with JSON lists.
        token_manager (ContextWindowTokenManager): The token manager for handling chat tokens.
        sequence (List[ChatModelResponse]): The list of ChatModelResponse objects.

    Properties:
        system_message (ChatModelResponse): The system message at the beginning of the sequence.
        token_count (int): The total count of tokens in the sequence.

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
    ):
        """
        Initializes a new TranscriptManager instance.

        Args:
            file_path (str): The file path to the JSON file used to store chat completion data.
            provider (str): The provider or source of chat completions.
            config (ConfigurationManager): The configuration manager for accessing settings and configurations.
            chat_model (ChatModel): The chat model used for managing chat completions.
        """
        super().__init__(file_path, provider, config, chat_model)
