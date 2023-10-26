"""
tests/unit/model/test_llama_cpp.py
"""
import pytest

from pygptprompt.model.base import (
    ChatModel,
    ChatModelEmbedding,
    ChatModelEncoding,
    ChatModelResponse,
)
from pygptprompt.model.llama_cpp import LlamaCppModel


class TestLlamaCppAPI:
    def test_api_type(self, llama_cpp_model: LlamaCppModel):
        assert isinstance(llama_cpp_model, ChatModel)

    @pytest.mark.slow
    def test_get_chat_completion(
        self,
        llama_cpp_model: LlamaCppModel,
        messages: list[ChatModelResponse],
    ):
        message: ChatModelResponse = llama_cpp_model.get_chat_completion(
            messages=messages
        )

        assert message["role"] == "assistant"
        assert isinstance(message["content"], str)
        assert message["content"] != ""

    @pytest.mark.slow
    def test_get_embedding(
        self,
        llama_cpp_model: LlamaCppModel,
        embedding_input: str,
    ):
        embedding: ChatModelEmbedding = llama_cpp_model.get_embedding(
            input=embedding_input
        )

        assert isinstance(embedding, list)
        assert len(embedding) > 0  # Ensure the List is not empty

        for sub_embedding in embedding:
            assert isinstance(sub_embedding, list)

            assert len(sub_embedding) > 0  # Ensure sub-list is not empty

            for value in sub_embedding:
                assert isinstance(value, float)

    @pytest.mark.slow
    def test_get_encoding(
        self,
        llama_cpp_model: LlamaCppModel,
        encoding_input: str,
    ):
        encoding: ChatModelEncoding = llama_cpp_model.get_encoding(text=encoding_input)

        assert isinstance(encoding, list)
        assert len(encoding) > 0  # Ensure the List is not empty

        for value in encoding:
            assert isinstance(value, int)

    @pytest.mark.slow
    def test_get_chat_completion_with_empty_messages(
        self,
        llama_cpp_model: LlamaCppModel,
    ):
        with pytest.raises(
            ValueError, match="'messages' argument cannot be empty or None"
        ):
            llama_cpp_model.get_chat_completion(messages=[])

    @pytest.mark.slow
    def test_get_embedding_with_empty_input(
        self,
        llama_cpp_model: LlamaCppModel,
    ):
        with pytest.raises(
            ValueError, match="'input' argument cannot be empty or None"
        ):
            llama_cpp_model.get_embedding(input="")
