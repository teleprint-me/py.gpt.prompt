"""
pygptprompt/api/openai.py
"""
import sys
from typing import Iterator, List, Union

import openai
from llama_cpp import ChatCompletionChunk, ChatCompletionMessage, EmbeddingData

from pygptprompt import logging
from pygptprompt.api.base import BaseAPI
from pygptprompt.config.manager import ConfigurationManager


class OpenAIAPI(BaseAPI):
    """
    API class for interacting with the OpenAI language models.

    Args:
        config (ConfigurationManager): The configuration manager instance.

    Attributes:
        config (ConfigurationManager): The configuration manager instance.
    """

    def __init__(self, config: ConfigurationManager):
        self.config = config
        openai.api_key = config.get_api_key()

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

    def get_completions(self, prompt: str):
        """
        Get completions from the OpenAI language models.

        Raises:
            NotImplementedError: This method is not implemented in the OpenAIAPI class.
        """
        raise NotImplementedError

    def get_chat_completions(
        self,
        messages: List[ChatCompletionMessage],
    ) -> ChatCompletionMessage:
        """
        Generate chat completions using the OpenAI language models.

        Args:
            messages (List[ChatCompletionMessage]): The list of chat completion messages.

        Returns:
            ChatCompletionMessage: The generated chat completion message.
        """
        if not messages:
            raise KeyError("Messages is a required argument.")

        try:
            # Call the OpenAI API's /v1/chat/completions endpoint
            response = openai.ChatCompletion.create(
                messages=messages,
                model=self.config.get_value(
                    "openai.chat_completions.model", "gpt-3.5-turbo"
                ),
                temperature=self.config.get_value(
                    "openai.chat_completions.temperature", 0.8
                ),
                max_tokens=self.config.get_value(
                    "openai.chat_completions.max_tokens", 1024
                ),
                top_p=self.config.get_value("openai.chat_completions.top_p", 0.95),
                n=self.config.get_value("openai.chat_completions.n", 1),
                stop=self.config.get_value("openai.chat_completions.stop", []),
                presence_penalty=self.config.get_value(
                    "openai.chat_completions.presence_penalty", 0
                ),
                frequency_penalty=self.config.get_value(
                    "openai.chat_completions.frequency_penalty", 0
                ),
                logit_bias=self.config.get_value(
                    "openai.chat_completions.logit_bias", {}
                ),
                stream=True,  # NOTE: Always coerce streaming
            )
            return self._stream_chat_completion(response)
        except Exception as e:
            logging.error(f"Error generating chat completions: {e}")
            return ChatCompletionMessage(role="error", content=str(e))

    def get_embeddings(self, input: Union[str, list[str]]) -> EmbeddingData:
        """
        Generate embeddings using the OpenAI language models.

        Args:
            input (Union[str, list[str]]): The input text or list of texts to generate embeddings for.

        Returns:
            EmbeddingData: The generated embedding vector.
        """
        if not input:
            raise KeyError("Input is a required argument.")

        try:
            # Call the OpenAI API's /v1/embeddings endpoint
            response = openai.Embedding.create(
                input=input,
                model=self.config.get_value(
                    "openai.embedding.model", "text-embedding-ada-002"
                ),
            )
            return EmbeddingData(**response["data"][0])
        except Exception as e:
            logging.error(f"Error generating embeddings: {e}")
            return EmbeddingData(index=0, object="list", embedding=[])
