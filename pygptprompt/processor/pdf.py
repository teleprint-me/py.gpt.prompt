"""
pygptprompt/processor/pdf.py
"""
import nltk
import spacy
from poppler import load_from_file


class PDFProcessor:
    def __init__(
        self,
        file_path: str,
        max_length: int,
        spacy_model: str = "en_core_web_sm",
        language: str = "english",
    ):
        self.file_path = file_path
        self.max_length = max_length
        self.spacy_model = spacy_model
        self.language = language

    def convert_pdf_to_text(self) -> list[str]:
        """
        Convert a PDF document into a list of strings, where each string is the text of a page.
        Returns:
            A list of strings representing the text of each page in the PDF.
        """
        pages: list[str] = []
        pdf_document = load_from_file(file_name=self.file_path)
        for index in range(pdf_document.pages):
            page = pdf_document.create_page(index)
            pages.append(page.text())
        return pages

    def chunk_text_with_spacy(self, text: str):
        """
        Split a text into chunks that are less than max_length using sentence segmentation from spaCy.
        Args:
            text: The input text to be chunked.
        Returns:
            A list of strings representing the text chunks.
        """
        nlp = spacy.load(self.spacy_model)
        doc = nlp(text)

        chunks = []
        current_chunk = ""
        for sentence in doc.sents:
            if len(current_chunk) + len(sentence.text) <= self.max_length:
                # If the current sentence fits in the current chunk, add it
                current_chunk += " " + sentence.text
            else:
                # If the current sentence doesn't fit in the current chunk, start a new chunk
                chunks.append(current_chunk.strip())
                current_chunk = sentence.text

        # Don't forget to add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def chunk_text_with_nltk(self, text: str) -> list[str]:
        """
        Split a text into chunks that are less than max_length. This version splits the text up into
        sentences and then combines those sentences to form chunks that are at most max_length long.
        Args:
            text: The input text to be chunked.
        Returns:
            A list of strings representing the text chunks.
        """
        # Split the text into sentences
        sentences = nltk.sent_tokenize(text, language=self.language)

        # Combine sentences into chunks that are at most max_length long
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.max_length:
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
