"""
pygptprompt/cli/pdf.py
"""
import os
from logging import Logger
from pathlib import Path
from typing import Dict, List, Union

import click

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.processor.pdf import PDFPage, PDFPageChunk, PDFProcessor


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
    metavar="CONFIG_PATH",
)
@click.argument(
    "pdf_path",
    type=click.Path(exists=True),
    metavar="PDF_PATH",
)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default="",
    metavar="OUTPUT_PATH",
    help="Path to the output text file. (default: empty)",
)
@click.option(
    "-s",
    "--session-name",
    type=click.STRING,
    default="",
    metavar="SESSION_LABEL",
    help="Specify a session label for the database collection and JSON files. (default: empty)",
)
@click.option(
    "--max-chunk-length",
    type=click.INT,
    default=256,
    metavar="CHUNK_LENGTH",
    help="The maximum length of each text chunk. (default: 256)",
)
@click.option(
    "--provider",
    type=click.STRING,
    default="llama_cpp",
    metavar="PROVIDER",
    help="The provider for the chat model. Options: llama_cpp, openai. (default: llama_cpp)",
)
@click.option(
    "--view-chunks",
    is_flag=True,
    help="View the raw text chunks without processing by the model.",
)
def main(
    config_path,
    pdf_path,
    output,
    session_name,
    max_chunk_length,
    provider,
    view_chunks,
):
    """
    Convert a PDF document into text and print or save the processed text.
    """
    # Check if the input PDF file exists
    if not os.path.isfile(pdf_path) or not pdf_path.endswith(".pdf"):
        click.echo("Error: The provided PDF path is invalid or does not exist.")
        return

    # Load configuration
    config = ConfigurationManager(config_path)

    # Setup logger
    logger: Logger = config.get_logger("general", Path(__file__).stem)

    # Create the chat model
    chat_model_factory = ChatModelFactory(config)
    chat_model = chat_model_factory.create_model(provider)

    # Create the PDF processor
    processor = PDFProcessor(
        session_name,
        max_chunk_length,
        provider,
        config,
        chat_model,
    )

    # Convert PDF to text
    pages: List[PDFPage] = processor.convert_pdf_to_text()
    pages = processor.convert_pages_to_chunks(pages, max_chunk_length)

    if output:
        # Save the processed text to the specified output file
        with open(output, "a+") as text_file:
            for page in pages:
                text_file.write(page)
    elif view_chunks:
        # View the raw text chunks without processing by the model
        click.echo("--- Raw Text Chunks ---")
        for index, page in enumerate(pages):
            click.echo(f"Page {index + 1} Chunks:")
            for chunk in page["chunks"]:
                click.echo(chunk)
                click.echo("---")
    else:
        # Print the processed text chunks
        click.echo("--- Processed Text Chunks ---")
        for index, page in enumerate(pages):
            # Process the text chunks with the chat model
            processed_chunks, metadata = processor.chunk_text_with_chat_model(
                page["text"], page["metadata"]
            )
            page["metadata"] = metadata

            click.echo(f"Page {index + 1} Chunks:")
            for chunk in processed_chunks:
                click.echo(chunk)
                click.echo("---")


if __name__ == "__main__":
    main()
