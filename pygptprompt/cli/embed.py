"""
pygptprompt/cli/embed.py

This script provides functionality for ingesting documents,
generating embeddings, and persisting them to the Chroma database.
"""

import logging
from logging import Logger
from pathlib import Path

import click
from chromadb.api.types import Documents, QueryResult

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import ChatModel
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.model.sequence.token_manager import TokenManager
from pygptprompt.storage.chroma import ChromaVectorStore


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
)
@click.argument(
    "source_path",
    type=click.STRING,
)
@click.option(
    "--session_name",
    "-s",
    type=click.STRING,
    default="default",
    help="Label for the database collection and associated JSON files.",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(
        [
            "openai",
            "llama_cpp",
            "huggingface",
            "torch",
        ]
    ),
    default="llama_cpp",
    help="Specify the model provider to use. Options include 'openai' for GPT models, 'llama_cpp' for quantized models supported by llama.cpp, 'huggingface' for Hugging Face models, and 'torch' for other PyTorch models like Facebook's Llama model.",
)
def main(
    config_path,
    session_name,
    provider,
    source_path,
    database_path,
):
    session_name: str = session_name

    config: ConfigurationManager = ConfigurationManager(config_path)

    logger: Logger = config.get_logger("general", Path(__file__).stem)
    logger.info(f"Using Session: {session_name}")
    logger.info(f"Using Config: {config_path}")
    logger.info(f"Using Provider: {provider}")
    logger.info(f"Using Database: {database_path}")
    logger.info(f"Loading documents from {source_path}")

    model_factory: ChatModelFactory = ChatModelFactory(config)
    chat_model: ChatModel = model_factory.create_model(provider)

    token_manager: TokenManager = TokenManager(provider, config, chat_model)

    vector_store: ChromaVectorStore = ChromaVectorStore(
        collection_name=session_name,
        config=config,
        chat_model=chat_model,
    )

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
    vector_store.upsert_to_collection(
        documents=documents,
        ids=["doc1", "doc2", "doc3"],
    )
    query = "synthetic document"
    results: QueryResult = vector_store.query_from_collection(
        query_texts=[query], n_results=2
    )

    print(f"Document IDs: {results['ids']}")
    if results["documents"]:
        print(f"Document Texts: {results['documents']}")
    if results["distances"]:
        print(f"Similarity Scores: {results['distances']}")

    logging.info(f"Loaded {len(documents)} documents from {source_path}")
    logging.info("Embeddings persisted to Chroma database.")


if __name__ == "__main__":
    main()
