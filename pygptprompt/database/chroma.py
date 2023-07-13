"""
pygptprompt/database/chroma.py

This module provides functionality for loading and persisting
documents to the Chroma database.

Classes:
- ChromaDBLoader: A class for loading and persisting documents to the Chroma database.

The ChromaDBLoader class handles loading documents, generating
embeddings using different embedding models, and persisting the
documents along with their embeddings to the Chroma database.

Usage:
    # Example usage of ChromaDBLoader
    loader = ChromaDBLoader(
        source_directory="path/to/source",
        persist_directory="path/to/database",
        embedding_model="huggingface/model",
        embedding_type="HuggingFaceInstructEmbeddings",
        device_type="cuda",
    )

    # Load the vector store retriever
    retriever = loader.load_retriever()

    # Persist a list of documents to the Chroma database
    documents = [document1, document2, document3]
    loader.persist(documents)
"""

from chromadb.config import Settings

from pygptprompt import EMBEDDINGS_MODEL, PATH_DATABASE, PATH_SOURCE, TORCH_DEVICE_TYPE


class ChromaDBLoader:
    """
    ChromaDBLoader class handles loading and persisting documents to Chroma database.

    Args:
        source_directory (str, optional): Directory path for source documents.
            Defaults to SOURCE_DIRECTORY.

        persist_directory (str, optional): Directory path for persisting the database.
            Defaults to PERSIST_DIRECTORY.

        embedding_model (str, optional): Name of the embedding model.
            Defaults to DEFAULT_EMBEDDING_MODEL.

        embedding_type (str, optional): Type of the embedding.
            Defaults to DEFAULT_EMBEDDING_TYPE.

        device_type (str, optional): Device type for embeddings.
            Defaults to DEFAULT_DEVICE_TYPE.
    """

    def __init__(
        self,
        path_source: str | None,
        path_database: str | None,
        embeddings_model: str | None,
        torch_device_type: str | None,
    ):
        self.source_directory = path_source or PATH_SOURCE
        self.persist_directory = path_database or PATH_DATABASE
        self.embedding_model = embeddings_model or EMBEDDINGS_MODEL
        self.device_type = torch_device_type or TORCH_DEVICE_TYPE

        # The settings for the Chroma database
        # - chroma_db_impl: Chroma database implementation (duckdb+parquet)
        # - persist_directory: Directory for persisting the database
        # - anonymized_telemetry: Whether anonymized telemetry is enabled (False)
        self.settings: Settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False,
        )

    def load_embedding_function(self) -> Embeddings | None:
        """
        Load the embedding function based on the specified embedding type.

        Returns:
            Optional[Embeddings]: Embeddings object for the specified embedding type.

        Raises:
            AttributeError: If an unsupported embedding type is provided.
        """
        if self.embedding_type in MAP_EMBEDDINGS_CLASS.keys():
            cls_EmbeddingType = MAP_EMBEDDINGS_CLASS[self.embedding_type]
            return cls_EmbeddingType(
                model_name=self.embedding_model,
                model_kwargs={"device": self.device_type},
            )
        else:
            raise AttributeError(
                f"Unsupported embeddings type provided: {self.embedding_type}"
            )

    def load_retriever(self) -> VectorStoreRetriever:
        """
        Load the vector store retriever from the Chroma database.

        Returns:
            VectorStoreRetriever: VectorStoreRetriever object.
        """
        database = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.load_embedding_function(),
            client_settings=self.settings,
        )
        return database.as_retriever()

    def load_retrieval_qa(self, llm: BaseLanguageModel) -> BaseRetrievalQA:
        """
        Loads a retrieval-based question answering model.

        Args:
            llm (BaseLanguageModel): The language model for answering questions.

        Returns:
            BaseRetrievalQA: The retrieval-based question answering model.
        """
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.load_retriever(),
            return_source_documents=True,
        )

    def persist(self, documents: list[Document]) -> None:
        """
        Persist the documents and their embeddings to the Chroma database.

        Args:
            documents (List[Document]): List of Document objects to be persisted.
        """
        # Persist the embeddings to Chroma database
        database = Chroma.from_documents(
            documents=documents,
            embedding=self.load_embedding_function(),
            persist_directory=str(self.persist_directory),
            client_settings=self.settings,
        )
        database.persist()
