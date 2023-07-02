# pygptprompt/api/ggml/requests.py
import os
import sys
from typing import Dict, Iterator, Union

from huggingface_hub import hf_hub_download
from llama_cpp import (
    ChatCompletion,
    ChatCompletionChunk,
    Completion,
    CompletionChunk,
    Llama,
)

from pygptprompt import PATH_HOME, logging

LlamaMessage = dict[str, str]

LlamaCompletion = Union[str, Completion]

LlamaChatCompletion = Union[
    Dict[str, str],
    ChatCompletion,
]

LlamaResponse = Union[
    str,
    Dict[str, str],
    Completion,
    ChatCompletion,
]


class LlamaCppRequests:
    def __init__(
        self,
        repo_id: str,
        filename: str,
        **kwargs,
    ):
        self.repo_id = repo_id
        self.filename = filename
        self.cache_dir = os.path.join(PATH_HOME, ".cache", "huggingface", "hub")
        self.model_path = self._download_model()
        self.llama_model = Llama(model_path=self.model_path, **kwargs)

    def _download_model(self) -> str:
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

    def _stream_completion(
        self,
        response_generator: Iterator[CompletionChunk],
    ) -> str:
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
        self,
        response_generator: Iterator[ChatCompletionChunk],
    ) -> LlamaMessage:
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

        return {"role": "assistant", "content": content}

    def _get_completions(self, **kwargs) -> LlamaCompletion:
        if "prompt" not in kwargs or not kwargs["prompt"]:
            raise ValueError("Prompt cannot be empty or None.")

        try:
            response = self.llama_model.create_completion(**kwargs)
            if not isinstance(response, Completion):
                response = self._stream_completion(response)
        except Exception as e:
            logging.error(f"Error generating completions: {e}")
            return str(e)

        return response

    def _get_chat_completions(self, **kwargs) -> LlamaChatCompletion:
        if "messages" not in kwargs or not kwargs["messages"]:
            raise ValueError("Messages cannot be empty or None.")

        try:
            response = self.llama_model.create_chat_completion(**kwargs)
            if not isinstance(response, ChatCompletion):
                response = self._stream_chat_completion(response)
        except Exception as e:
            logging.error(f"Error generating chat completions: {e}")
            return dict(error=str(e))

        return response

    def get(
        self,
        endpoint: str = "completions",
        **kwargs,
    ) -> LlamaResponse:
        if endpoint == "completions":
            return self._get_completions(**kwargs)
        elif endpoint == "chat_completions":
            return self._get_chat_completions(**kwargs)
        elif endpoint == "embedding":
            raise NotImplementedError(f"llama.cpp: {endpoint}")
        else:
            raise ValueError(f"Invalid Endpoint: {endpoint}")
