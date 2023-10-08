"""
pygptprompt/function/sqlite.py

This module defines the SQLiteMemoryFunction class, which provides methods for querying and updating memory records in an SQLite database.

# Usage:
from pygptprompt.config.manager import ConfigurationManager

config = ConfigurationManager("tests/config.dev.json")

chat_model_memory = SQLiteMemoryFunction("test", config)

# Query a memory with a given key
memory_result = chat_model_memory.query_memory("some_key")

# Update a memory with a given key and new content
chat_model_memory.update_memory("some_key", "new_content")
"""
from datetime import datetime

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.storage.sqlite import Model, OperationalError, SQLiteMemoryStore


class SQLiteMemoryFunction:
    """
    Provides methods for querying and updating memory records in an SQLite database.

    Args:
        table_name (str): The name of the database table storing memory records.
        database_path (str): The path to the SQLite database file.
        config (ConfigurationManager): An instance of ConfigurationManager for logging.

    Attributes:
        table_name (str): The name of the database table storing memory records.
        model (Model): The SQLite database model for memory records.
    """

    def __init__(
        self,
        table_name: str,
        config: ConfigurationManager,
    ):
        database = SQLiteMemoryStore(config)
        self._model = database.get_model("memory", table_name)
        self._logger = config.get_logger("general", self.__class__.__name__)

    @property
    def model(self) -> Model:
        """
        Get the SQLite database model for memory records.

        Returns:
            Model: The database model for memory records.
        """
        return self._model

    def get_all_keys(self) -> str:
        """
        Retrieve all the keys from the memory records in the database.

        Returns:
            str: A formatted string representing the list of keys for direct LLM consumption.

        Raises:
            OperationalError: If an error occurs while querying the database.
        """
        try:
            keys = [memory.key for memory in self.model.select(self.model.key)]

            # Format the list of keys into a structured string
            formatted_keys = "\n".join(keys)
            return f"Available Memory Keys:\n{formatted_keys}"

        except OperationalError as message:
            self._logger.exception(message)
            return f"Error: {message}"

    def query_memory(self, key: str) -> str:
        """
        Query a memory record with a given key from the database.

        Args:
            key (str): The key to identify the memory record.

        Returns:
            str: A formatted string containing the timestamp and content of the memory record.

        Raises:
            OperationalError: If an error occurs while querying the database.
        """
        try:
            memory = self.model.select().where(self.model.key == key).get()
            return f"---\n{memory.timestamp}:\n---\n{memory.content}"

        except self.model.DoesNotExist:
            self._logger.warning(f"No memory found for key: {key}")
            return f"No memory found for key: {key}"

        except OperationalError as message:
            self._logger.exception(message)
            return f"Error: {message}"

    def update_memory(self, key: str, content: str) -> str:
        """
        Update or create a memory record with a given key and content in the database.

        Args:
            key (str): The key to identify the memory record.
            content (str): The content to be stored in the memory record.

        Returns:
            str: A message indicating the success or failure of the update operation.

        Raises:
            OperationalError: If an error occurs while updating the database.
        """
        try:
            memory, created = self.model.get_or_create(
                key=key, defaults={"content": content, "timestamp": datetime.now()}
            )

            if not created:
                memory.content = content
                memory.timestamp = datetime.now()
                memory.save()

            self._logger.info(f"Memory updated for key: {key}")
            return f"Memory updated for key: {key}"

        except OperationalError as message:
            self._logger.exception(message)
            return f"Error: Failed to update memory for key: {key}"

    def delete_memory(self, key: str) -> str:
        """
        Delete a memory record with a given key from the database.

        Args:
            key (str): The key to identify the memory record to be deleted.

        Returns:
            str: A message indicating the success or failure of the deletion operation.

        Raises:
            OperationalError: If an error occurs while deleting from the database.
        """
        try:
            query = self.model.delete().where(self.model.key == key)
            num_deleted = query.execute()

            if num_deleted:
                self._logger.info(f"Memory deleted for key: {key}")
                return f"Memory deleted for key: {key}"
            else:
                self._logger.warning(f"No memory found for key: {key}")
                return f"No memory found for key: {key}"

        except OperationalError as message:
            self._logger.exception(message)
            return f"Error: Failed to delete memory for key: {key}"
