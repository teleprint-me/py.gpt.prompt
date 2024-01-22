"""
pygptprompt/processor/pdf.py
"""
import os
from typing import Any, Dict, List

import magic
import tqdm
from poppler import load_from_file

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import ChatModel, ChatModelResponse
from pygptprompt.model.sequence.context_manager import ContextWindowManager


class ChatModelChunkProcessor:
    def __init__(
        self,
        context_file_path: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        # NOTE: Chat Models can make function calls
        self.chat_model = chat_model
        # Context Window will keep track of text based sequences
        self.context_window = self._initialize_context_window(
            context_file_path=context_file_path,
            provider=provider,
            config=config,
        )
        # Track messages within the context window
        self.messages = self._initialize_messages()

    def _initialize_messages(self) -> List[ChatModelResponse]:
        self.system_prompt = ChatModelResponse(
            role="system",
            content="System task: Process and repair the given text chunks.",
        )
        return [self.system_prompt]

    def _initialize_context_window(
        self,
        context_file_path: str,
        provider: str,
        config: ConfigurationManager,
    ):
        # NOTE: context_window automatically dequeues messages exceeding
        # chat models max sequence length.
        return ContextWindowManager(
            file_path=context_file_path,
            provider=provider,
            config=config,
            chat_model=self.chat_model,
            vector_store=None,
        )

    def process_chunk(self, chunk: str, meta_prompt: str) -> str:
        instruct_prompt = ChatModelResponse(
            role="user",
            content=f"Repair and summarize the following text:\n\n{chunk}\n\n{meta_prompt}",
        )

        self.messages.append(instruct_prompt)
        chat_model_response = self.chat_model.get_chat_completion(self.messages)
        self.context_window.enqueue(chat_model_response)
        return chat_model_response["content"]


class PDFProcessor:
    def __init__(
        self,
        input_file_path: str,
        context_file_path: str,
        chunk_size: int,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        # Set the chat model provider
        self.provider = provider
        # Setup the chat model configuration
        self.config = config
        # Set the document i/o file paths
        self.input_file_path = input_file_path  # a pdf or directory
        # Set the chunk size
        self.chunk_size = chunk_size
        # Chunk processor assists chat model with document processing
        self.chunk_processor = ChatModelChunkProcessor(
            context_file_path, provider=provider, config=config, chat_model=chat_model
        )

    def scan_directory_for_pdfs(self, directory: str) -> List[str]:
        """Get all pdf files from within a given directory"""
        # If "file_path" is a single pdf source, ignore this method.
        # If "file_path" is a directory, get all pdfs within directory.
        pdf_files = []
        for root, dirs, files in os.walk(directory):
            for file in tqdm.tqdm(files, desc="Scanning files"):
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
        pages = []
        pdf_document = load_from_file(file_name=self.input_file_path)
        for index in tqdm.tqdm(range(pdf_document.pages), desc="Converting PDF"):
            page = pdf_document.create_page(index)
            meta = {
                "pdf_id": self.input_file_path.split("/")[-1],
                "page_number": index,
                "num_chunks": 0,
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
        text_length = len(text)
        total_chunks = (
            text_length + self.chunk_size - 1
        ) // self.chunk_size  # Calculate total number of chunks

        # Initialize tqdm progress bar
        with tqdm.tqdm(total=total_chunks, desc="Processing Chunks") as pbar:
            while start < text_length:
                end = min(start + self.chunk_size, text_length)
                chunk = text[start:end]

                # Generate dynamic prompt based on metadata
                prompt = f"PDF ID: {metadata['pdf_id']}, Page: {metadata['page_number']}, Chunk: {len(chunk) + 1}"

                # Process the chunk with the model
                processed_chunk = self.chunk_processor.process_chunk(chunk, prompt)
                chunks.append(processed_chunk)

                # Update tqdm progress bar
                pbar.update(1)  # Increment by one chunk

                start = end

        # Update metadata
        metadata["num_chunks"] = len(chunks)

        return chunks, metadata
