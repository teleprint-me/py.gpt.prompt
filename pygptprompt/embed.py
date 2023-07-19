"""
pygptprompt/embed.py

This script provides functionality for ingesting documents,
generating embeddings, and persisting them to the Chroma database.
"""

import logging

import click
from chromadb import API, Client, Settings
from chromadb.api.models.Collection import Collection
from chromadb.api.types import Documents, QueryResult

from pygptprompt import PATH_DATABASE, PATH_SOURCE


@click.command()
@click.option(
    "--path_source",
    default=PATH_SOURCE,
    type=click.STRING,
    help=f"The path the documents are read from (default: {PATH_SOURCE})",
)
@click.option(
    "--path_database",
    default=PATH_DATABASE,
    type=click.STRING,
    help=f"The path the embeddings are written to (default: {PATH_DATABASE})",
)
def main(
    path_source,
    path_database,
    embeddings_model,
    torch_device_type,
    torch_triton_type,
):
    # Using model and types
    logging.info(f"Using Embedding Model: {embeddings_model}")
    logging.info(f"Using Device Type: {torch_device_type}")
    logging.info(f"Device Type is Triton: {torch_triton_type}")

    name: str = "my_collection"

    # Uses PostHog library to collect telemetry
    settings: Settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=str(path_database),
        anonymized_telemetry=False,
    )

    chroma_client: API = Client(settings=settings)

    try:
        collection: Collection = chroma_client.create_collection(name=name)
    except ValueError:
        logging.info(f"Collection with name {name} already exists")
        exit(1)

    # Load documents and split them into chunks
    logging.info(f"Loading documents from {path_source}")

    documents: Documents = [
        "This is the first synthetic document.",
        "Here is another synthetic document.",
        "This is the third synthetic document.",
    ]

    # Each document needs a unique ID
    ids: list[str] = ["doc1", "doc2", "doc3"]

    collection.add(documents=documents, ids=ids)

    query = "synthetic document"
    results: QueryResult = collection.query(query_texts=[query], n_results=2)

    print(f"Document IDs: {results['ids']}")
    if results["documents"]:
        print(f"Document Texts: {results['documents']}")
    if results["distances"]:
        print(f"Similarity Scores: {results['distances']}")

    logging.info(f"Loaded {len(documents)} documents from {path_source}")
    # logging.info(f"Split into {len(texts)} chunks of text")

    # logging.info("Embeddings persisted to Chroma database.")


if __name__ == "__main__":
    main()
