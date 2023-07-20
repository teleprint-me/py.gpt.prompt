"""
tests/unit/test_api_openai.py
"""
import pytest
from llama_cpp import ChatCompletionMessage, EmbeddingData

from pygptprompt.api.base import BaseAPI
from pygptprompt.api.openai import OpenAIAPI


class TestOpenAI:
    def test_api_type(self, openai_api: OpenAIAPI):
        assert isinstance(openai_api, BaseAPI)

    @pytest.mark.private
    def test_streaming_completions(
        self,
        openai_api: OpenAIAPI,
        chat_completion: list[ChatCompletionMessage],
    ):
        message: ChatCompletionMessage = openai_api.get_chat_completions(
            messages=chat_completion,
        )

        print()

        assert bool(message)
        print(message)
        assert (
            message["content"]
            == "Le renard brun rapide a sauté par-dessus le chien paresseux."
        )

    @pytest.mark.private
    def test_get_embeddings(
        self,
        openai_api: OpenAIAPI,
        embedding_input: str,
    ):
        data: EmbeddingData = openai_api.get_embeddings(
            input=embedding_input,
        )

        assert isinstance(data["index"], int)
        assert data["object"] == "embedding"
        assert isinstance(data["embedding"], list)
