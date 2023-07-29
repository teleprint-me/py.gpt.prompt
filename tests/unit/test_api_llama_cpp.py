"""
tests/unit/test_api_llama_cpp.py
"""
import pytest
from llama_cpp import ChatCompletionMessage, Embedding, EmbeddingData

from pygptprompt.api.base import BaseAPI
from pygptprompt.api.llama_cpp import LlamaCppAPI


class TestLlamaCppAPI:
    def test_api_type(self, llama_cpp_api: LlamaCppAPI):
        assert isinstance(llama_cpp_api, BaseAPI)

    @pytest.mark.slow
    def test_get_chat_completions(
        self,
        llama_cpp_api: LlamaCppAPI,
        messages: list[ChatCompletionMessage],
    ):
        message: ChatCompletionMessage = llama_cpp_api.get_chat_completions(
            messages=messages
        )

        assert message["role"] == "assistant"
        assert isinstance(message["content"], str)
        assert message["content"] != ""

    @pytest.mark.slow
    def test_get_embeddings(
        self,
        llama_cpp_api: LlamaCppAPI,
        embedding_input: str,
    ):
        embedding: Embedding = llama_cpp_api.get_embeddings(input=embedding_input)

        assert embedding["object"] == "list"
        assert isinstance(embedding["data"], list)

        data: EmbeddingData = embedding["data"][0]

        assert isinstance(data["index"], int)
        assert data["object"] == "embedding"
        assert isinstance(data["embedding"], list)
        assert len(data["embedding"]) > 0  # Ensure the List is not empty

    @pytest.mark.slow
    def test_get_chat_completions_with_empty_messages(
        self,
        llama_cpp_api: LlamaCppAPI,
    ):
        with pytest.raises(
            ValueError, match="'messages' argument cannot be empty or None"
        ):
            llama_cpp_api.get_chat_completions(messages=[])

    @pytest.mark.slow
    def test_get_embeddings_with_empty_input(
        self,
        llama_cpp_api: LlamaCppAPI,
    ):
        with pytest.raises(
            ValueError, match="'input' argument cannot be empty or None"
        ):
            llama_cpp_api.get_embeddings(input="")
