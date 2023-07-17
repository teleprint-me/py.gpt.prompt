"""
pygptprompt/api/llama.py
"""
import os
import sys
from pathlib import Path
from typing import Iterator

from huggingface_hub import hf_hub_download
from llama_cpp import ChatCompletionChunk, ChatCompletionMessage, Embedding, Llama

from pygptprompt import logging
from pygptprompt.api.base import BaseAPI


class LlamaAPI(BaseAPI):
    """
    API class for interacting with the Llama language model.

    Args:
        repo_id (str): The ID of the model repository.
        filename (str): The name of the model file.
        **kwargs: Additional keyword arguments.

    Attributes:
        repo_id (str): The ID of the model repository.
        filename (str): The name of the model file.
        cache_dir (str): The directory to cache the downloaded model.
        model_path (str): The path to the downloaded model file.
        llama_model (Llama): The Llama language model instance.
    """

    def __init__(self, repo_id: str, filename: str, **kwargs):
        self.repo_id = repo_id
        self.filename = filename

        if "cache_dir" in kwargs:
            self.cache_dir = kwargs["cache_dir"]
        else:
            self.cache_dir = os.path.join(Path.home(), ".cache", "huggingface", "hub")

        if "model_path" in kwargs["model_path"]:
            self.model_path = kwargs["model_path"]
        else:
            self.model_path = self._download_model()

        if "verbose" not in kwargs:
            kwargs["verbose"] = False  # Coerce silent output

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

    def get_completions(self, **kwargs):
        """
        Get completions from the Llama language model.

        Raises:
            NotImplementedError: This method is not implemented in the LlamaAPI class.
        """
        raise NotImplementedError

    def get_chat_completions(self, **kwargs) -> ChatCompletionMessage:
        """
        Generate chat completions using the Llama language model.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            ChatCompletionMessage: The generated chat completion message.

        Raises:
            ValueError: If the 'messages' argument is empty or None.

        Note:
            This method always coerces streaming by setting 'stream' to True.
        """
        if "messages" not in kwargs or not kwargs["messages"]:
            raise ValueError("Messages cannot be empty or None.")

        try:
            kwargs["stream"] = True  # NOTE: Always coerce streaming
            response = self.llama_model.create_chat_completion(**kwargs)
            return self._stream_chat_completion(response)
        except Exception as e:
            logging.error(f"Error generating chat completions: {e}")
            return ChatCompletionMessage(role="assistant", content=str(e))

    def get_embeddings(self, **kwargs) -> Embedding:
        """
        Generate embeddings using the Llama language model.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            Embedding: The generated embedding.

        Raises:
            ValueError: If the 'input' argument is empty or None.
        """
        # NOTE: `input` is required and is type `Union[str, List[str]]`.
        if "input" not in kwargs or not kwargs["input"]:
            raise ValueError("Input cannot be empty or None.")

        return self.llama_model.create_embedding(kwargs["input"])
