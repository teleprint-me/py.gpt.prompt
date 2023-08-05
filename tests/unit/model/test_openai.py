"""
tests/unit/model/test_openai.py
"""
import json
from typing import List

import pytest

from pygptprompt.model.openai import OpenAIModel
from pygptprompt.pattern.model import ChatModel
from pygptprompt.pattern.types import (
    ChatModelChatCompletion,
    ChatModelEmbedding,
    ChatModelEncoding,
)


class TestOpenAI:
    def test_api_type(self, openai_model: OpenAIModel):
        assert isinstance(openai_model, ChatModel)

    @pytest.mark.private
    def test_get_chat_completion(
        self,
        openai_model: OpenAIModel,
        chat_completion: List[ChatModelChatCompletion],
    ):
        message: ChatModelChatCompletion = openai_model.get_chat_completion(
            messages=chat_completion,
        )

        print()

        assert bool(message)
        print(message)
        assert "Le renard brun rapide" in message["content"]
        assert "chien paresseux" in message["content"]

    @pytest.mark.private
    def test_get_chat_completion_function(
        self,
        openai_model: OpenAIModel,
        function_completion: List[ChatModelChatCompletion],
        mock_weather_callback: object,
    ):
        # Call the get_chat_completions method
        assistant_message: ChatModelChatCompletion = openai_model.get_chat_completion(
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
    def test_get_embedding(
        self,
        openai_model: OpenAIModel,
        embedding_input: str,
    ):
        embedding: ChatModelEmbedding = openai_model.get_embedding(
            input=embedding_input,
        )
        print(embedding)

        assert isinstance(embedding, list)
        assert len(embedding) > 0  # Ensure the List is not empty

        for sub_embedding in embedding:
            assert isinstance(sub_embedding, list)

            assert len(sub_embedding) > 0  # Ensure sub-list is not empty

            for value in sub_embedding:
                assert isinstance(value, float)

    @pytest.mark.private
    def test_get_encoding(
        self,
        openai_model: OpenAIModel,
        encoding_input: str,
    ):
        encoding: ChatModelEncoding = openai_model.get_encoding(text=encoding_input)

        assert isinstance(encoding, list)
        assert len(encoding) > 0  # Ensure the List is not empty

        for value in encoding:
            assert isinstance(value, int)

    @pytest.mark.private
    def test_get_chat_completion_with_empty_messages(
        self,
        openai_model: OpenAIModel,
    ):
        with pytest.raises(
            ValueError, match="'messages' argument cannot be empty or None"
        ):
            openai_model.get_chat_completion(messages=[])

    @pytest.mark.private
    def test_get_embedding_with_empty_input(
        self,
        openai_model: OpenAIModel,
    ):
        with pytest.raises(
            ValueError, match="'input' argument cannot be empty or None"
        ):
            openai_model.get_embedding(input="")
