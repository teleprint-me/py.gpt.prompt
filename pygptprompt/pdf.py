"""
pygptprompt/pdf.py
"""
import os

import click

from pygptprompt.processor.pdf import PDFProcessor


@click.command()
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
    "--chunk_length",
    type=click.INT,
    default=256,
    help="The maximum length of each chunk.",
)
@click.option(
    "--spacy_model",
    type=click.STRING,
    default="en_core_web_sm",
    help="The spaCy model to use for sentence segmentation.",
)
def main(path_input, path_output, chunk_length, spacy_model):
    """
    Convert a PDF document into text and print the text of the first page.
    """
    if not path_input:
        print("A valid file path must be given as an argument.")
        exit(1)
    if not os.path.isfile(path_input) or not path_input.endswith(".pdf"):
        print("The path must point to a valid PDF file.")
        exit(1)

    processor = PDFProcessor(path_input, chunk_length, spacy_model)

    pages = processor.convert_pdf_to_text()

    chunks = []
    for page in pages:
        chunks.extend(processor.chunk_text_with_spacy(page))

    if path_output:
        with open(path_output, "w") as text_file:
            for chunk in chunks:
                text_file.write(chunk + "\n\n")
    else:
        print("---")
        for index, chunk in enumerate(chunks):
            print(index)
            print(chunk)
            print("---")


if __name__ == "__main__":
    main()
