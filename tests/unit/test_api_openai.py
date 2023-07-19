"""
tests/unit/test_api_openai.py
"""
import pytest
from llama_cpp import ChatCompletionMessage, EmbeddingData

from pygptprompt.api.openai import OpenAIAPI


class TestOpenAI:
    @pytest.mark.private
    def test_streaming_completions(
        self,
        openai_api: OpenAIAPI,
        chat_completion: list[ChatCompletionMessage],
    ):
        model = "gpt-3.5-turbo"
        temperature = 0
        max_tokens = 128

        message: ChatCompletionMessage = openai_api.get_chat_completions(
            messages=chat_completion,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        print()

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
        model = "text-embedding-ada-002"

        data: EmbeddingData = openai_api.get_embeddings(
            model=model,
            input=embedding_input,
        )

        assert isinstance(data["index"], int)
        assert data["object"] == "embedding"
        assert isinstance(data["embedding"], list)
