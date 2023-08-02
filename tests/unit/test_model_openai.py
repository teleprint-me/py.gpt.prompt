"""
tests/unit/test_api_openai.py
"""
import json
from typing import List

import pytest
from llama_cpp import ChatCompletionMessage, Embedding, EmbeddingData

from pygptprompt.model.openai import OpenAIModel
from pygptprompt.pattern.model import ChatModel


class TestOpenAI:
    def test_api_type(self, openai_api: OpenAIModel):
        assert isinstance(openai_api, ChatModel)

    @pytest.mark.private
    def test_streaming_completions(
        self,
        openai_api: OpenAIModel,
        chat_completion: List[ChatCompletionMessage],
    ):
        message: ChatCompletionMessage = openai_api.get_chat_completion(
            messages=chat_completion,
        )

        print()

        assert bool(message)
        print(message)
        assert "Le renard brun rapide" in message["content"]
        assert "chien paresseux" in message["content"]

    @pytest.mark.private
    def test_streaming_functions(
        self,
        openai_api: OpenAIModel,
        function_completion: List[ChatCompletionMessage],
        mock_weather_callback: object,
    ):
        # Call the get_chat_completions method
        assistant_message: ChatCompletionMessage = openai_api.get_chat_completion(
            messages=function_completion
        )

        # Check if the role is 'function'
        assert assistant_message["role"] == "function"

        # Extract the function name and arguments
        function_name = assistant_message["function_call"]
        function_args = json.loads(assistant_message["function_args"])

        # Check if the function name is 'get_current_weather'
        assert function_name == "get_current_weather"

        # Call the mock function with the extracted arguments
        response = mock_weather_callback(**function_args)

        # Check if the response is as expected
        assert (
            response
            == "The current weather in San Francisco, CA is 20 degrees celsius."
        )

    @pytest.mark.private
    def test_get_embeddings(
        self,
        openai_api: OpenAIModel,
        embedding_input: str,
    ):
        embedding: Embedding = openai_api.get_embedding(
            input=embedding_input,
        )

        assert embedding["object"] == "list"
        assert isinstance(embedding["data"], list)

        data: EmbeddingData = embedding["data"][0]

        assert isinstance(data["index"], int)
        assert data["object"] == "embedding"
        assert isinstance(data["embedding"], List)
        assert len(data["embedding"]) > 0  # Ensure the List is not empty

    @pytest.mark.private
    def test_get_chat_completions_with_empty_messages(
        self,
        openai_api: OpenAIModel,
    ):
        with pytest.raises(
            ValueError, match="'messages' argument cannot be empty or None"
        ):
            openai_api.get_chat_completion(messages=[])

    @pytest.mark.private
    def test_get_embeddings_with_empty_input(
        self,
        openai_api: OpenAIModel,
    ):
        with pytest.raises(
            ValueError, match="'input' argument cannot be empty or None"
        ):
            openai_api.get_embedding(input="")
