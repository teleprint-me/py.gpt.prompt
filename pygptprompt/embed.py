"""
pygptprompt/embed.py

This script provides functionality for ingesting documents,
generating embeddings, and persisting them to the Chroma database.
"""

import logging

import click
from chromadb import API, PersistentClient, Settings
from chromadb.api.models.Collection import Collection
from chromadb.api.types import Documents, QueryResult

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.pattern.model import ChatModel, ChatModelEmbeddingFunction


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
    default="config.json",
)
@click.option(
    "--path_source",
    type=click.STRING,
    help="The path the documents are read from.",
)
@click.option(
    "--path_database",
    type=click.STRING,
    default="database",
    help="The path the embeddings are written to.",
)
@click.option(
    "--provider",
    type=click.STRING,
    default="llama_cpp",
    help="The provider to generate embeddings with.",
)
def main(
    config_path,
    path_source,
    path_database,
    provider,
):
    config: ConfigurationManager = ConfigurationManager(config_path)

    factory: ChatModelFactory = ChatModelFactory(config)
    chat_model: ChatModel = factory.create_model(provider)
    embedding_function: ChatModelEmbeddingFunction = ChatModelEmbeddingFunction(
        chat_model=chat_model
    )

    name: str = "my_collection"

    # Load documents and split them into chunks
    logging.info(f"Loading documents from {path_source}")

    # NOTE: Imagine that documents are messages
    documents: Documents = [
        "This is the first synthetic document.",
        "Here is another synthetic document.",
        "This is the third synthetic document.",
    ]

    # Each document needs a unique ID
    # NOTE: We can use the role as a part of the ID
    # This will require something thoughtful to make
    # each role reference unique. Maybe the position/index
    # within the transcript?
    ids: list[str] = ["doc1", "doc2", "doc3"]

    # Uses PostHog library to collect telemetry
    chroma_client: API = PersistentClient(
        path=path_database,
        settings=Settings(anonymized_telemetry=False),
    )

    try:
        collection: Collection = chroma_client.create_collection(
            name=name, embedding_function=embedding_function
        )

        collection.add(documents=documents, ids=ids)
    except ValueError:
        logging.info(f"Collection with name {name} already exists")
        collection: Collection = chroma_client.get_collection(
            name=name, embedding_function=embedding_function
        )

    query = "synthetic document"
    results: QueryResult = collection.query(query_texts=[query], n_results=2)

    print(f"Document IDs: {results['ids']}")
    if results["documents"]:
        print(f"Document Texts: {results['documents']}")
    if results["distances"]:
        print(f"Similarity Scores: {results['distances']}")

    logging.info(f"Loaded {len(documents)} documents from {path_source}")
    logging.info("Embeddings persisted to Chroma database.")


if __name__ == "__main__":
    main()
