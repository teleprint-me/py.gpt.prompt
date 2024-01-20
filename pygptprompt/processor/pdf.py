"""
pygptprompt/processor/pdf.py
"""
import os
from typing import Any, Dict, List

import magic
from poppler import load_from_file

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import ChatModel, ChatModelResponse
from pygptprompt.model.sequence.context_manager import ContextWindowManager


class ChatModelChunkProcessor:
    def __init__(
        self,
        chat_model: ChatModel,
        context_window: ContextWindowManager,
    ):
        self.chat_model = chat_model
        self.context_window = context_window

    def process_chunk(self, chunk: str) -> str:
        system_prompt = ChatModelResponse(
            role="system",
            content="System task: Process and repair the given text chunks.",
        )

        instruct_prompt = ChatModelResponse(
            role="user", content=f"Repair and summarize the following text:\n\n{chunk}"
        )

        chat_model_request = [system_prompt, instruct_prompt]

        chat_model_response = self.chat_model.get_chat_completion(chat_model_request)

        self.context_window.enqueue(chat_model_response)

        return chat_model_response["content"]


class PDFProcessor:
    def __init__(
        self,
        input_file_path: str,
        output_file_path: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        # Set the provider
        self.provider = provider
        # Setup the config
        self.config = config
        # Set the i/o file paths
        self.input_file_path = input_file_path  # a pdf or directory
        self.output_file_path = output_file_path  # where the transcript is saved to
        # NOTE: Chat Models can make function calls
        self.chat_model = chat_model
        # Context Window will keep track of text based sequences
        context_window = self._initialize_context_window(
            provider=provider, config=config
        )
        self.chunk_processor = ChatModelChunkProcessor(
            chat_model=chat_model, context_window=context_window
        )

    def _initialize_context_window(self, provider: str, config: ConfigurationManager):
        ContextWindowManager(
            file_path=self.output_file_path,
            provider=provider,
            config=self.config,
            chat_model=self.chat_model,
            vector_store=None,
        )

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
        pdf_document = load_from_file(file_name=self.input_file_path)
        for index in range(pdf_document.pages):
            page = pdf_document.create_page(index)
            meta = {
                "pdf_id": self.input_file_path.split("/")[-1],  # or any identifier
                "page_number": index,
                "num_chunks": 0,  # to be updated
            }
            pages.append({"text": page.text(), "metadata": meta})
        return pages

    def chunk_text_with_chat_model(self, text: str, metadata: dict):
        """
        Split a text into chunks and process them with the chat model.
        Updates the metadata to include the number of chunks generated.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]

            # Generate dynamic prompt based on metadata
            prompt = f"PDF ID: {metadata['pdf_id']}, Page: {metadata['page_number']}, Chunk: {len(chunks) + 1}"

            # Process the chunk with the model
            processed_chunk = self.chat_model.process_chunk(chunk, prompt)

            chunks.append(processed_chunk)

            start = end

        # Update metadata
        metadata["num_chunks"] = len(chunks)

        return chunks, metadata  # now returns updated metadata
