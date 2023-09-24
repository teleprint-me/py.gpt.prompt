"""
pygptprompt/processor/pdf.py
"""
import os
from typing import Any, Dict, List

import magic
from poppler import load_from_file

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.pattern.model import ChatModel, ChatModelResponse
from pygptprompt.session.token import ChatSessionTokenManager


class PDFProcessor:
    def __init__(
        self,
        file_path: str,
        provider: str,
        config: ConfigurationManager,
        language: str = "English",
    ):
        # Initialize chat model
        model_factory = ChatModelFactory(config)
        # NOTE: Chat Models can make function calls
        self.chat_model = model_factory.create_model(provider)
        # Token manager will keep track of text based sequences
        self.token_manager = ChatSessionTokenManager(provider, config, self.chat_model)
        self.file_path = file_path  # a pdf or directory
        self.language = language

    def scan_directory_for_pdfs(self, directory: str) -> List[str]:
        """Get all pdf files from within a given directory"""
        # If "file_path" is a single pdf source, ignore this method.
        # If "file_path" is a directory, get all pdfs within directory.
        pdf_files: List[str] = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                mime = magic.Magic()
                mime_type = mime.from_file(file_path)
                if "pdf" in mime_type.lower():
                    pdf_files.append(file_path)
        return pdf_files

    def convert_pdf_to_text(self) -> List[Dict[str, Any]]:
        """
        Convert a PDF document into a list of dictionaries, where each dictionary
        contains the text of a page and metadata like pdf_id, page_number, and num_chunks.
        """
        pages: List[Dict[str, Any]] = []
        pdf_document = load_from_file(file_name=self.file_path)
        for index in range(pdf_document.pages):
            page = pdf_document.create_page(index)
            meta = {
                "pdf_id": self.file_path.split("/")[-1],  # or any identifier
                "page_number": index,
                "num_chunks": 0,  # to be updated
            }
            pages.append({"text": page.text(), "metadata": meta})
        return pages

    def chunk_text_with_chat_model(self, text: str, metadata: Dict):
        """
        Split a text into chunks that are less than max_length using your chat model.
        Updates the metadata to include the number of chunks generated.
        """
        # Your chat model-based chunking algorithm here
        chunks = []
        # ... logic to fill chunks and count tokens

        # Update metadata
        metadata["num_chunks"] = len(chunks)

        return chunks, metadata  # now returns updated metadata
