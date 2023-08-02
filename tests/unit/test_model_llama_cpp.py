"""
tests/unit/test_api_llama_cpp.py
"""
import pytest
from llama_cpp import ChatCompletionMessage, Embedding, EmbeddingData

from pygptprompt.model.llama_cpp import LlamaCppModel
from pygptprompt.pattern.model import ChatModel


class TestLlamaCppAPI:
    def test_api_type(self, llama_cpp_api: LlamaCppModel):
        assert isinstance(llama_cpp_api, ChatModel)

    @pytest.mark.slow
    def test_get_chat_completions(
        self,
        llama_cpp_api: LlamaCppModel,
        messages: list[ChatCompletionMessage],
    ):
        message: ChatCompletionMessage = llama_cpp_api.get_chat_completion(
            messages=messages
        )

        assert message["role"] == "assistant"
        assert isinstance(message["content"], str)
        assert message["content"] != ""

    @pytest.mark.slow
    def test_get_embeddings(
        self,
        llama_cpp_api: LlamaCppModel,
        embedding_input: str,
    ):
        embedding: Embedding = llama_cpp_api.get_embedding(input=embedding_input)

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
        llama_cpp_api: LlamaCppModel,
    ):
        with pytest.raises(
            ValueError, match="'messages' argument cannot be empty or None"
        ):
            llama_cpp_api.get_chat_completion(messages=[])

    @pytest.mark.slow
    def test_get_embeddings_with_empty_input(
        self,
        llama_cpp_api: LlamaCppModel,
    ):
        with pytest.raises(
            ValueError, match="'input' argument cannot be empty or None"
        ):
            llama_cpp_api.get_embedding(input="")
