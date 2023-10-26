"""
pygptprompt/storage/chroma.py
"""
from datetime import datetime
from typing import Dict, List, Optional, Union

from chromadb import PersistentClient, Settings
from chromadb.api.types import Include, OneOrMany, QueryResult, Where, WhereDocument

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import ChatModel, ChatModelDocument, ChatModelDocuments
from pygptprompt.storage.function import VectorStoreEmbeddingFunction


# NOTE:
# TELEMETRY IS SET TO OFF BY DEFAULT.
# YOU MUST OPT IN IF YOU WANT THIS TURNED ON.
#
# I plan on removing telemetry completely in the future.
# When I do, Chroma will be removed completely as a result.
#
# Set anonymized_telemetry in your clients settings to
# False to opt out of telemetry.
#
# SOURCE: https://docs.trychroma.com/telemetry
#
class ChromaVectorStore:
    """
    A class for managing the Chroma vector store.

    This class is responsible for managing interactions with the Chroma vector store, including
    adding messages to the store and querying stored vectors.

    Args:
        collection_name (str): The name of the collection in the Chroma vector store.
        database_path (str): The path to the Chroma database.
        config (ConfigurationManager): The configuration manager for accessing settings and configurations.
        chat_model (ChatModel): The chat model used for embedding messages.
        anonymized_telemetry (bool, optional): Whether anonymized telemetry should be enabled. Default is False.

    Attributes:
        collection_name (str): The name of the collection in the Chroma vector store.
        database_path (str): The path to the Chroma database.
        config (ConfigurationManager): The configuration manager for accessing settings and configurations.
        chat_model (ChatModel): The chat model used for embedding messages.
        anonymized_telemetry (bool): Whether anonymized telemetry is enabled.
        embedding_function (VectorStoreEmbeddingFunction): The function for embedding messages.
        chroma_client (PersistentClient): The Chroma database client.
        collection: The collection in the Chroma vector store.

    Methods:
        get_chroma_heartbeat(): Get the Chroma service timestamp.
        get_collection_count(): Get the total number of embeddings in the collection.
        add_message_to_collection(message: dict): Add a message to the collection.
        upsert_to_collection(ids, metadatas, documents): Upsert documents to the collection.
        query_from_collection(query_texts, n_results, where, where_document, include): Query the collection for documents.
    """

    def __init__(
        self,
        collection_name: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
        anonymized_telemetry: bool = False,
    ):
        # Initialize attributes
        self.collection_name = collection_name
        self.config = config
        self.chat_model = chat_model
        self.anonymized_telemetry = anonymized_telemetry
        self.database_path = config.evaluate_path("app.database.chroma")
        self.embedding_function = None
        self.chroma_client = None
        self.collection = None

        # Initialize logger
        self.logger = self.config.get_logger("general", self.__class__.__name__)

        # Initialize components
        self._initialize_components()
        self._get_or_create_collection()  # avoid cascades

    def _initialize_components(self):
        # Initialize embedding function
        self.embedding_function = VectorStoreEmbeddingFunction(
            chat_model=self.chat_model, logger=self.logger
        )

        # Initialize Chroma client
        self.chroma_client = PersistentClient(
            path=self.database_path,
            settings=Settings(
                anonymized_telemetry=self.anonymized_telemetry,
            ),
        )

    def _get_or_create_collection(self):
        try:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
            )
            self.logger.debug(f"Created collection {self.collection_name}")
        except ValueError:
            self.collection = self.chroma_client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
            )
            self.logger.debug(f"Loaded collection {self.collection_name}")

    def get_chroma_heartbeat(self) -> int:
        """
        Get the Chroma service timestamp.

        Returns:
            int: The Chroma service timestamp.
        """
        return self.chroma_client.heartbeat()

    def get_collection_count(self) -> int:
        """
        Get the total number of embeddings in a collection.

        Returns:
            int: The total number of embeddings in the collection.
        """
        return self.collection.count()

    def add_message_to_collection(self, message: dict):
        """
        Add a message to the collection.

        Args:
            message (dict): The message to be added to the collection.
        """
        timestamp = datetime.utcnow().isoformat()
        unique_id = f"{self.collection_name}_{timestamp}"

        self.collection.add(
            ids=[unique_id],
            documents=[message["content"]],
            metadatas=[{"role": message["role"]}],
        )

        self.logger.debug(
            f"Added message to collection {self.collection_name} with ID {unique_id}"
        )

    def upsert_to_collection(
        self,
        ids: Union[str, List[str]],
        metadatas: Union[Dict[str, str], List[Dict[str, str]]],
        documents: Union[ChatModelDocument, ChatModelDocuments],
    ):
        """
        Upsert documents to the collection.

        New items will be added, and existing items will be updated.

        Args:
            ids (Union[str, List[str]]): The IDs of the documents to upsert.
            metadatas (Union[Dict[str, str], List[Dict[str, str]]]): The metadata of the documents.
            documents (Union[ChatModelDocument, ChatModelDocuments]): The documents to upsert.
        """
        self.collection.upsert(
            ids=ids,
            metadatas=metadatas,
            documents=documents,
        )

        self.logger.debug(
            f"Upserted documents to collection {self.collection_name} with ID {ids}"
        )

    def query_from_collection(
        self,
        query_texts: Optional[OneOrMany[ChatModelDocument]] = None,
        n_results: int = 10,
        where: Optional[Where] = None,
        where_document: Optional[WhereDocument] = None,
        include: Include = ["metadatas", "documents", "distances"],
    ) -> QueryResult:
        """
        Query the collection for documents.

        Args:
            query_texts (Optional[OneOrMany[ChatModelDocument]]): The query texts.
            n_results (int): The number of results to retrieve. Default is 10.
            where (Optional[Where]): The where condition for the query. Default is None.
            where_document (Optional[WhereDocument]): The where document for the query. Default is None.
            include (Include): The elements to include in the query result. Default is ["metadatas", "documents", "distances"].

        Returns:
            QueryResult: The query result.
        """
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=include,
        )
