"""
pygptprompt/api/openai.py
"""
import sys
from typing import Any, Iterator

import openai
from llama_cpp import ChatCompletionMessage

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
        self, response_generator: Iterator[dict[str, Any]]
    ) -> ChatCompletionMessage:
        """
        Process the stream of chat completion chunks and return the generated message.

        Args:
            response_generator (Iterator[dict[str, Any]]): The chat completion chunk stream.

        Returns:
            ChatCompletionMessage: The generated message.
        """
        content = ""

        for stream in response_generator:
            try:
                token = stream.choices[0].delta["content"]

                if stream.choices[0].delta:
                    print(token, end="")
                    sys.stdout.flush()
                    content += token
            except KeyError:
                continue

        print()
        sys.stdout.flush()

        return ChatCompletionMessage(role="assistant", content=content)

    def get_completions(self, **kwargs):
        """
        Get completions from the OpenAI language models.

        Raises:
            NotImplementedError: This method is not implemented in the OpenAIAPI class.
        """
        raise NotImplementedError

    def get_chat_completions(
        self,
        **kwargs,
    ) -> ChatCompletionMessage:
        """
        Generate chat completions using the OpenAI language models.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            ChatCompletionMessage: The generated chat completion message.

        Raises:
            KeyError: If the 'messages' argument is missing.
        """
        if "model" not in kwargs:
            kwargs["model"] = "gpt-3.5-turbo"

        if "messages" not in kwargs:
            raise KeyError("Messages is a required argument.")

        if "stream" not in kwargs:
            kwargs["stream"] = True

        # Call the OpenAI API's chat.completion endpoint
        response = openai.ChatCompletion.create(**kwargs)
        # Return the generated message
        return self._stream_chat_completion(response)

    def get_embeddings(self, **kwargs):
        """
        Generate embeddings using the OpenAI language models.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            List[float]: The generated embedding vector.

        Raises:
            KeyError: If the 'input' argument is missing.
        """
        if "model" not in kwargs:
            kwargs["model"] = "text-embedding-ada-002"

        if "input" not in kwargs:
            raise KeyError("Input is a required argument.")

        # Call the OpenAI API's embeddings endpoint
        response = openai.Embedding.create(**kwargs)
        # Return the embedding vector
        return response["data"][0]["embedding"]
