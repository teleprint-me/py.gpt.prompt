"""
tests/unit/test_api_llama_cpp.py
"""
import pytest
from llama_cpp import ChatCompletionMessage, EmbeddingData

from pygptprompt.api.llama_cpp import LlamaCppAPI


class TestLlamaCppAPI:
    @pytest.mark.slow
    def test_get_chat_completions(
        self,
        llama_cpp_api: LlamaCppAPI,
        messages: list[ChatCompletionMessage],
    ):
        message: ChatCompletionMessage = llama_cpp_api.get_chat_completions(
            messages=messages,
            max_tokens=128,
            temperature=0.8,
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
        data: EmbeddingData = llama_cpp_api.get_embeddings(input=embedding_input)

        assert isinstance(data["index"], int)
        assert data["object"] == "list"
        assert isinstance(data["embedding"], list)
