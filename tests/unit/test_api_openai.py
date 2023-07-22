"""
tests/unit/test_api_openai.py
"""
import json
from typing import List

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
        chat_completion: List[ChatCompletionMessage],
    ):
        message: ChatCompletionMessage = openai_api.get_chat_completions(
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
        openai_api: OpenAIAPI,
        function_completion: List[ChatCompletionMessage],
        mock_weather_callback: object,
    ):
        # Call the get_chat_completions method
        assistant_message: ChatCompletionMessage = openai_api.get_chat_completions(
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
        openai_api: OpenAIAPI,
        embedding_input: str,
    ):
        data: EmbeddingData = openai_api.get_embeddings(
            input=embedding_input,
        )

        assert isinstance(data["index"], int)
        assert data["object"] == "embedding"
        assert isinstance(data["embedding"], List)
        assert len(data["embedding"]) > 0  # Ensure the List is not empty

    @pytest.mark.private
    def test_get_chat_completions_with_empty_messages(
        self,
        openai_api: OpenAIAPI,
    ):
        with pytest.raises(
            ValueError, match="'messages' argument cannot be empty or None"
        ):
            openai_api.get_chat_completions(messages=[])

    @pytest.mark.private
    def test_get_embeddings_with_empty_input(
        self,
        openai_api: OpenAIAPI,
    ):
        with pytest.raises(
            ValueError, match="'input' argument cannot be empty or None"
        ):
            openai_api.get_embeddings(input="")
