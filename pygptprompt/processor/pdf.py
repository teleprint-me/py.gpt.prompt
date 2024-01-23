"""
pygptprompt/processor/pdf.py
"""
import os
from typing import Any, Dict, List, TypedDict

import magic
import poppler
import tqdm

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import ChatModel, ChatModelResponse
from pygptprompt.model.sequence.session_manager import SessionManager


class PDFMetaData(TypedDict):
    id: str
    index: int
    total: int


class PDFPageChunk(TypedDict):
    text: str
    metadata: PDFMetaData


class PDFPage(TypedDict):
    text: str
    metadata: PDFMetaData
    chunks: List[PDFPageChunk] = []

    def add_chunk(self, chunk: PDFPageChunk):
        self.chunks.append(chunk)


class ChatModelChunkProcessor:
    def __init__(
        self,
        session_name: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        # NOTE: Chat Models can make function calls
        self.chat_model = chat_model
        # Context Window will keep track of text based sequences
        self.session_manager = SessionManager(
            session_name=session_name,
            provider=provider,
            config=config,
            chat_model=self.chat_model,
            vector_store=None,
        )
        # Track messages within the context window
        self.session_manager.system_message = ChatModelResponse(
            role="system",
            content="System task: Repair and improve the given text segments.",
        )

    def _generate_prompt(self, page: PDFPage, chunk: PDFPageChunk) -> str:
        """
        Generate a prompt based on the provided metadata.
        """
        page_metadata = page.metadata
        chunk_metadata = chunk.metadata

        # Construct a prompt using metadata
        prompt = (
            f"PDF ID: {page_metadata.id}, Page: {page_metadata.index}, "
            f"Chunk: {chunk_metadata.index} out of {chunk_metadata.total}"
        )
        return prompt

    def _generate_instruction(
        self, page: PDFPage, chunk: PDFPageChunk
    ) -> ChatModelResponse:
        metadata_prompt = self._generate_prompt(page, chunk)
        instruction = (
            "Repair and improve the following text segments to make them coherent and complete. "
            "Focus on clarity and correctness."
        )
        return ChatModelResponse(
            role="user", content=f"{instruction}\n\n{chunk.text}\n\n{metadata_prompt}"
        )

    def process_chunk(self, page: PDFPage, chunk: PDFPageChunk) -> str:
        instruct_prompt = self._generate_instruction(page, chunk)
        self.session_manager.enqueue(instruct_prompt)
        # NOTE: The session_manager automatically dequeues messages
        # exceeding chat models max sequence length.
        chat_model_response = self.chat_model.get_chat_completion(
            self.session_manager.sequence
        )
        self.session_manager.enqueue(chat_model_response)
        return chat_model_response["content"]


class PDFProcessor:
    def __init__(
        self,
        session_name: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
        chunk_length: int,
    ):
        # Chunk processor assists chat model with document processing
        self.chunk_processor = ChatModelChunkProcessor(
            session_name,
            provider,
            config,
            chat_model,
        )
        # Set the chunk size
        self.chunk_length = chunk_length

    def scan_directory_for_pdfs(self, directory: str) -> List[str]:
        """Get all pdf files from within a given directory"""
        pdf_files = []
        for root, dirs, files in os.walk(directory):
            for file in tqdm.tqdm(files, desc="Scanning files"):
                file_path = os.path.join(root, file)
                mime = magic.Magic()
                mime_type = mime.from_file(file_path)
                if "pdf" in mime_type.lower():
                    pdf_files.append(file_path)
        return pdf_files

    def _extract_pdf_data(
        self,
        pdf_document: poppler.document.Document,
        pdf_id: str,
        page_number: int,
        total_pages,
    ) -> PDFPage:
        page = pdf_document.create_page(page_number)
        metadata = PDFMetaData(
            id=pdf_id,
            index=page_number,
            total=total_pages,
        )
        return PDFPage(text=page.text(), metadata=metadata)

    def convert_pdf_to_text(self, pdf_path: str) -> List[PDFPage]:
        """
        Convert a PDF document into a list of dictionaries, where each dictionary contains the text of a page and metadata like pdf_id, page_number, etc.
        """
        pages = []
        pdf_document = poppler.load_from_file(file_name=pdf_path)
        pdf_id = pdf_path.split("/")[-1]
        total_pages = pdf_document.pages()

        for index in tqdm.tqdm(range(total_pages), desc="Converting PDF"):
            pdf_data = self._extract_pdf_data(pdf_document, pdf_id, index, total_pages)
            pages.append(pdf_data)

        return pages

    def _extract_pdf_page_data(
        self,
        page: PDFPage,
        page_chunk: str,
        chunk_index: int,
        total_chunks: int,
    ) -> PDFPageChunk:
        metadata = PDFMetaData(
            id=page.metadata.id,
            chunk_index=chunk_index + 1,
            total_chunks=total_chunks,
        )
        return PDFPageChunk(
            text=page_chunk,
            metadata=metadata,
        )

    def convert_text_to_chunks(self, page: PDFPage, chunk_length: int) -> PDFPage:
        start = 0
        text_length = len(page.text)
        total_chunks = (text_length + chunk_length - 1) // chunk_length

        for chunk_index in tqdm.tqdm(range(total_chunks), desc="Converting PDF Page"):
            end = min(start + chunk_length, text_length)
            chunk = page.text[start:end]

            pdf_page_chunk = self._extract_pdf_page_data(
                page, chunk, chunk_index, total_chunks
            )
            page.add_chunk(pdf_page_chunk)
            start = end

        return page

    def convert_pages_to_chunks(
        self, pages: List[PDFPage], chunk_length: int
    ) -> List[PDFPage]:
        index = 0
        while index < len(pages):
            pages[index] = self.convert_text_to_chunks(pages[index], chunk_length)
        return pages

    def process_pdf_with_chat_model(self, page: PDFPage):
        """
        Process a PDF page with the chat model.
        """
        # If view_chunks is False, process the chunks with the model
        processed_chunks = []

        for chunk in page.chunks:
            # Process the chunk with the model
            processed_chunk = self.chunk_processor.process_chunk(page, chunk)
            processed_chunks.append(processed_chunk)

        return processed_chunk
