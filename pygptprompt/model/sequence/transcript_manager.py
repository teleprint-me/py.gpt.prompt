"""
pygptprompt/model/sequence/transcript.py
"""
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.sequence.manager import SequenceManager


class TranscriptManager(SequenceManager):
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
        super().__init__(file_path, config)
