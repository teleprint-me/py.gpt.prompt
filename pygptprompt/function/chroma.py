"""
pygptprompt/function/chroma.py

This module defines the ChromaVectorFunction class, which provides methods for querying and updating a vector store used for managing conversational context in chat models.
"""
from typing import Dict, List, Optional, Union

from chromadb.api.types import Include, OneOrMany, Where, WhereDocument

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.model import ChatModel
from pygptprompt.storage.chroma import ChromaVectorStore


class ChromaVectorFunction:
    """
    Provides methods for querying and updating a vector store used for managing conversational context in chat models.

    Args:
        collection_name (str): The name of the collection in the vector store.
        database_path (str): The path to the vector database.
        config (ConfigurationManager): An instance of ConfigurationManager for configuration settings.
        chat_model (ChatModel): An instance of the ChatModel for context.

    Attributes:
        vector_store (ChromaVectorStore): The ChromaVectorStore instance for vector operations.
    """

    def __init__(
        self,
        collection_name: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        self.collection_name = collection_name
        self.vector_store = ChromaVectorStore(collection_name, config, chat_model)

    def query_collection(
        self,
        query_texts: Union[str, List[str]] = None,
        n_results: int = 5,
        where: Optional[Where] = None,
        where_document: Optional[WhereDocument] = None,
        include: Include = ["metadatas", "documents", "distances"],
    ) -> str:
        """
        Query the collection for documents.

        Args:
            query_texts (Optional[OneOrMany[str]]): The query texts.
            n_results (int): The number of results to retrieve. Default is 10.
            where (Optional[Where]): The where condition for the query. Default is None.
            where_document (Optional[WhereDocument]): The where document for the query. Default is None.
            include (Include): The elements to include in the query result. Default is ["metadatas", "documents", "distances"].

        Returns:
            str: A message indicating the result of the query.
        """
        results = self.vector_store.query_from_collection(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=where_document,
            include=include,
        )

        return f"Queried documents from {self.collection_name} with {results}"

    def upsert_to_collection(
        self,
        ids: Union[str, List[str]],
        metadatas: Union[Dict[str, str], List[Dict[str, str]]],
        documents: Union[str, List[str]],
    ) -> str:
        """
        Upsert documents to the collection.

        New items will be added, and existing items will be updated.

        Args:
            ids (Union[str, List[str]]): The IDs of the documents to upsert.
            metadatas (Union[Dict[str, str], List[Dict[str, str]]]): The metadata of the documents.
            documents (Union[ChatModelDocument, ChatModelDocuments]): The documents to upsert.

        Returns:
            str: A message indicating the result of the upsert operation.
        """
        self.vector_store.upsert_to_collection(
            ids=ids,
            metadatas=metadatas,
            documents=documents,
        )

        return f"Upserted documents to collection {self.collection_name} with ID {ids}"
