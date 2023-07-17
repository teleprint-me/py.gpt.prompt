import sys
from typing import Any, Iterator

import openai
from llama_cpp import ChatCompletionMessage

from pygptprompt.api.base import BaseAPI


class OpenAIAPI(BaseAPI):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def _stream_chat_completion(
        self, response_generator: Iterator[dict[str, Any]]
    ) -> ChatCompletionMessage:
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
        # For now, we'll raise a NotImplementedError
        # You can implement this method later if you decide to support completions
        raise NotImplementedError

    def get_chat_completions(
        self,
        **kwargs,
    ) -> ChatCompletionMessage:
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
        if "model" not in kwargs:
            kwargs["model"] = "text-embedding-ada-002"

        if "input" not in kwargs:
            raise KeyError("Input is a required argument.")

        # Call the OpenAI API's embeddings endpoint
        response = openai.Embedding.create(**kwargs)
        # Return the embedding vector
        return response["data"][0]["embedding"]
