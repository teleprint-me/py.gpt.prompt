"""
pygptprompt/cli/pdf.py
"""
import os

import click

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.processor.pdf import PDFProcessor


@click.command()
@click.argument(
    "path_config",
    type=click.Path(exists=True),
)
@click.option(
    "--path_input",
    type=click.STRING,
    default=str(),
    help="The path to the source document. Default is empty string.",
)
@click.option(
    "--path_output",
    type=click.STRING,
    default=str(),
    help="The path to the source document. Default is empty string.",
)
@click.option(
    "--path_context",
    type=click.STRING,
    default=str(),
    help="The path to the source document. Default is empty string.",
)
@click.option(
    "--chunk_size",
    type=click.INT,
    default=256,
    help="The maximum length of each chunk.",
)
@click.option(
    "--provider",
    type=click.STRING,
    default="llama_cpp",
    help="The provider for the chat model. llama_cpp or openai. default is llama_cpp.",
)
def main(path_input, path_output, chunk_size, provider, config_path):
    """
    Convert a PDF document into text and print the text of the first page.
    """
    if not path_input:
        print("A valid file path must be given as an argument.")
        exit(1)
    if not os.path.isfile(path_input) or not path_input.endswith(".pdf"):
        print("The path must point to a valid PDF file.")
        exit(1)

    config = ConfigurationManager(config_path)
    chat_model_factory = ChatModelFactory(config)
    chat_model = chat_model_factory.create_model(provider)

    processor = PDFProcessor(
        path_input,
        path_output,
        chunk_size,
        provider,
        config,
        chat_model,
    )

    pages = processor.convert_pdf_to_text()

    if path_output:
        with open(path_output, "a+") as text_file:
            for page in pages:
                text_file.write(page)
    else:
        chunks = []
        for page in pages:
            # Process the text chunks with the chat model
            processed_chunks, metadata = processor.chunk_text_with_chat_model(
                page["text"], page["metadata"]
            )
            chunks.extend(processed_chunks)

            # Update metadata with the number of chunks
            page["metadata"] = metadata

        # Print the processed chunks
        print("---")
        for index, chunk in enumerate(chunks):
            print(f"Chunk {index + 1}:")
            print(chunk)
            print("---")


if __name__ == "__main__":
    main()
