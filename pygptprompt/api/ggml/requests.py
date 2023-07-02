# pygptprompt/api/ggml/requests.py
import os
import sys
from typing import Iterator, Union

from huggingface_hub import hf_hub_download
from llama_cpp import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
    Completion,
    CompletionChunk,
    Llama,
)

from pygptprompt import PATH_HOME, logging

LlamaCompletion = Union[str, Completion]

LlamaChatCompletion = Union[ChatCompletion, ChatCompletionMessage]

LlamaResponse = Union[str, Completion, ChatCompletion, ChatCompletionMessage]


class LlamaCppRequests:
    def __init__(self, repo_id: str, filename: str, **kwargs):
        """
        Initialize LlamaCppRequests.

        Args:
            repo_id (str): The repository ID.
            filename (str): The filename of the model from the given repository.
            **kwargs: Additional arguments for Llama initialization.
        """
        self.repo_id = repo_id
        self.filename = filename
        self.cache_dir = os.path.join(PATH_HOME, ".cache", "huggingface", "hub")
        self.model_path = self._download_model()
        self.llama_model = Llama(model_path=self.model_path, **kwargs)

    def _download_model(self) -> str:
        """
        Download the model file if not already present in the cache.

        Returns:
            str: The path to the downloaded model file.
        """
        logging.info(f"Using {self.repo_id} to load {self.filename}")

        try:
            model_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.filename,
                cache_dir=self.cache_dir,
                resume_download=True,
            )
        except Exception as e:
            logging.error(f"Error downloading model: {e}")
            sys.exit(1)

        logging.info(f"Using {model_path} to load {self.repo_id} into memory")

        return model_path

    def _stream_completion(self, response_generator: Iterator[CompletionChunk]) -> str:
        """
        Process the stream of completion chunks and return the generated content.

        Args:
            response_generator (Iterator[CompletionChunk]): The completion chunk stream.

        Returns:
            str: The generated content.
        """
        content = ""

        for stream in response_generator:
            token = stream["choices"][0]["text"]
            if token:
                print(token, end="")
                sys.stdout.flush()
                content += token

        print()
        sys.stdout.flush()

        return content

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
                token = stream["choices"][0]["delta"]["content"]
                if token:
                    print(token, end="")
                    sys.stdout.flush()
                    content += token
            except KeyError:
                continue

        print()  # Add newline to model output
        sys.stdout.flush()

        return ChatCompletionMessage(role="assistant", content=content)

    def _get_completions(self, **kwargs) -> LlamaCompletion:
        """
        Generate completions for the given prompt.

        Args:
            **kwargs: Additional arguments for generating completions.

        Returns:
            LlamaCompletion: The generated completions.
        """
        if "prompt" not in kwargs or not kwargs["prompt"]:
            raise ValueError("Prompt cannot be empty or None.")

        try:
            response = self.llama_model.create_completion(**kwargs)
            if "stream" in kwargs and kwargs["stream"]:
                response = self._stream_completion(response)
        except Exception as e:
            logging.error(f"Error generating completions: {e}")
            return str(e)

        return response

    def _get_chat_completions(self, **kwargs) -> LlamaChatCompletion:
        """
        Generate chat completions for the given messages.

        Args:
            **kwargs: Additional arguments for generating chat completions.

        Returns:
            LlamaChatCompletion: The generated chat completions.
        """
        if "messages" not in kwargs or not kwargs["messages"]:
            raise ValueError("Messages cannot be empty or None.")

        try:
            response = self.llama_model.create_chat_completion(**kwargs)
            if "stream" in kwargs and kwargs["stream"]:
                response = self._stream_chat_completion(response)
        except Exception as e:
            logging.error(f"Error generating chat completions: {e}")
            return ChatCompletionMessage(role="assistant", content=str(e))

        return response

    def get(
        self,
        endpoint: str = "completions",
        **kwargs,
    ) -> LlamaResponse:
        """
        Perform a GET request to the Llama API.

        Args:
            endpoint (str): The API endpoint to access.
            **kwargs: Additional arguments for the API request.

        Returns:
            LlamaResponse: The response from the Llama API.
        """
        if endpoint == "completions":
            return self._get_completions(**kwargs)
        elif endpoint == "chat_completions":
            return self._get_chat_completions(**kwargs)
        elif endpoint == "embeddings":
            raise NotImplementedError(f"llama.cpp: {endpoint}")
        else:
            raise ValueError(f"Invalid Endpoint: {endpoint}")
