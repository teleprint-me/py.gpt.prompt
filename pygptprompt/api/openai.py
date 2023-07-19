"""
pygptprompt/api/openai.py
"""
import sys
from typing import Any, Iterator

import openai
from llama_cpp import ChatCompletionChunk, ChatCompletionMessage, EmbeddingData

from pygptprompt import logging
from pygptprompt.api.base import BaseAPI


class OpenAIAPI(BaseAPI):
    """
    API class for interacting with the OpenAI language models.

    Args:
        api_key (str): The OpenAI API key.

    Attributes:
        api_key (str): The OpenAI API key.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def _stream_chat_completion(
        self, response_generator: Iterator[ChatCompletionChunk]
    ) -> ChatCompletionMessage:
        """
        Process the stream of chat completion chunks and return the generated message.

        Args:
            response_generator (Iterator[ChatCompletionChunk]): The chat completion chunk stream.

        Returns:
            ChatCompletionMessage: The generated message.
        """
        content = ""

        for stream in response_generator:
            try:
                token = stream.choices[0].delta["content"]
                if token:
                    print(token, end="")
                    sys.stdout.flush()
                    content += token
            except KeyError:
                continue

        print()  # Add newline to model output
        sys.stdout.flush()

        return ChatCompletionMessage(role="assistant", content=content)

    def get_completions(self, **kwargs: Any):
        """
        Get completions from the OpenAI language models.

        Raises:
            NotImplementedError: This method is not implemented in the OpenAIAPI class.
        """
        raise NotImplementedError

    def get_chat_completions(
        self,
        **kwargs: Any,
    ) -> ChatCompletionMessage:
        """
        Generate chat completions using the OpenAI language models.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            ChatCompletionMessage: The generated chat completion message.

        Raises:
            KeyError: If the 'messages' argument is missing.

        Note:
            This method always coerces streaming by setting 'stream' to True.
        """
        if "model" not in kwargs:
            kwargs["model"] = "gpt-3.5-turbo"

        if "messages" not in kwargs:
            raise KeyError("Messages is a required argument.")

        kwargs["stream"] = True  # NOTE: Always coerce streaming

        try:
            # Call the OpenAI API's /v1/chat/completions endpoint
            response = openai.ChatCompletion.create(**kwargs)
            return self._stream_chat_completion(response)
        except Exception as e:
            logging.error(f"Error generating chat completions: {e}")
            return ChatCompletionMessage(role="error", content=str(e))

    def get_embeddings(self, **kwargs: Any) -> EmbeddingData:
        """
        Generate embeddings using the OpenAI language models.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            EmbeddingData: The generated embedding vector.

        Raises:
            KeyError: If the 'input' argument is missing.
        """
        if "model" not in kwargs:
            kwargs["model"] = "text-embedding-ada-002"

        if "input" not in kwargs:
            raise KeyError("Input is a required argument.")

        try:
            # Call the OpenAI API's /v1/embeddings endpoint
            response = openai.Embedding.create(**kwargs)
            return EmbeddingData(**response["data"][0])
        except Exception as e:
            logging.error(f"Error generating embeddings: {e}")
            return EmbeddingData(index=0, object="list", embedding=[])
