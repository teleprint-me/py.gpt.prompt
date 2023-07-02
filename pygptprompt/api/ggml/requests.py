# pygptprompt/api/ggml/requests.py
import os
import sys
from typing import Any, Dict, Optional

from huggingface_hub import hf_hub_download
from llama_cpp import ChatCompletionMessage, Llama

from pygptprompt import PATH_HOME, logging


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

    def _process_stream_response(self, response_generator) -> Dict[str, Any]:
        content = ""

        sys.stdout.flush()
        for stream in response_generator:
            try:
                token = stream["choices"][0]["delta"]["content"]
                if token:
                    print(token, end="")
                    sys.stdout.flush()
                    content += token
            except KeyError:
                continue
        print()  # Add padding between user input and assistant response
        sys.stdout.flush()
        return {"role": "assistant", "content": content}

    def get(endpoint: str = "completions", **kwargs) -> dict[str, Any]:
        # if stream is true, then returns a generator of dictionaries
        # matching the completions streaming api
        # if stream is false, then returns a dictionary matching
        # the OpenAI response object
        response_generator = self.llama_api.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
        )
