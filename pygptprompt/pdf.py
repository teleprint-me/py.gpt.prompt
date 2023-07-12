import os

import click
import nltk
from poppler import load_from_file


def normalize_indentation(chunks: list[str]) -> list[str]:
    """
    Normalize the indentation of the chunks. This function assumes that if a line has less leading
    whitespace than the previous line, it should be indented to the same level as the previous line.
    Args:
        chunks: A list of strings representing the text chunks to be normalized.

    Returns:
        A list of strings with normalized indentation.
    """
    normalized_chunks = []
    for chunk in chunks:
        lines = chunk.splitlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()
        normalized_chunks.append("\n".join(lines))
    return normalized_chunks


def chunk_text(text: str, max_length: int) -> list[str]:
    """
    Split a text into chunks that are less than max_length. This version splits the text up into
    sentences and then combines those sentences to form chunks that are at most max_length long.
    Args:
        text: The input text to be chunked.
        max_length: The maximum length of each chunk.

    Returns:
        A list of strings representing the text chunks.
    """
    # Split the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Combine sentences into chunks that are at most max_length long
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            # If the current sentence fits in the current chunk, add it
            current_chunk += " " + sentence
        else:
            # If the current sentence doesn't fit in the current chunk, start a new chunk
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    # Don't forget to add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def convert_pdf_to_text(file_path: str) -> list[str]:
    """
    Convert a PDF document into a list of strings, where each string is the text of a page.
    Args:
        file_path: The path to the PDF file.

    Returns:
        A list of strings representing the text of each page in the PDF.
    """
    pages: list[str] = []
    pdf_document = load_from_file(file_name=file_path)
    for index in range(pdf_document.pages):
        page = pdf_document.create_page(index)
        pages.append(page.text())
    return pages


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
def main(path_input, path_output):
    """
    Convert a PDF document into text and print the text of the first page.
    """
    if not path_input:
        print("A valid file path must be given as an argument.")
        exit(1)
    if not os.path.isfile(path_input) or not path_input.endswith(".pdf"):
        print("The path must point to a valid PDF file.")
        exit(1)

    pages = convert_pdf_to_text(path_input)
    for page in pages:
        print(page)
    chunks = []
    # for page in pages:
    #     chunks.extend(chunk_text(page, 512))  # or 256 for the MiniLM model
    # chunks = normalize_indentation(chunks)
    # print("---")
    # for index, chunk in zip(range(len(chunks)), chunks):
    #     print(index)
    #     print(chunk)
    #     print("---")


if __name__ == "__main__":
    main()
