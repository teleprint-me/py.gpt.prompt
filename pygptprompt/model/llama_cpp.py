"""
pygptprompt/model/llama_cpp.py
"""
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Union

from huggingface_hub import hf_hub_download
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)
from llama_cpp import ChatCompletionChunk, Llama

from pygptprompt import logging
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.model import (
    ChatModel,
    ChatModelChatCompletion,
    ChatModelEmbedding,
    ChatModelEncoding,
    ChatModelTextCompletion,
)


class LlamaCppModel(ChatModel):
    """
    ChatModel class for interacting with the Llama language model.

    Args:
        config (ConfigurationManager): The configuration manager instance.

    Attributes:
        repo_id (str): The ID of the model repository.
        filename (str): The name of the model file.
        cache_dir (str): The directory to cache the downloaded model.
        model_path (str): The path to the downloaded model file.
        model (Llama): The Llama language model instance.
    """

    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.repo_id = config.get_value(
            "llama_cpp.model.repo_id", "TheBloke/Llama-2-7B-Chat-GGML"
        )
        self.filename = config.get_value(
            "llama_cpp.model.filename", "llama-2-7b-chat.ggmlv3.q5_1.bin"
        )
        self.cache_dir = Path(Path.home(), ".cache", "huggingface", "hub")
        self.model_path = self._download_model()
        self.model = Llama(
            model_path=self.model_path,
            n_ctx=config.get_value("llama_cpp.model.n_ctx", 4096),
            n_batch=config.get_value("llama_cpp.model.n_batch", 512),
            n_gpu_layers=config.get_value("llama_cpp.model.n_gpu_layers", 0),
            low_vram=config.get_value("llama_cpp.model.low_vram", False),
            verbose=config.get_value("llama_cpp.model.verbose", False),
            n_parts=config.get_value("llama_cpp.model.n_parts", -1),
            seed=config.get_value("llama_cpp.model.seed", 1337),
            f16_kv=config.get_value("llama_cpp.model.f16_kv", True),
            logits_all=config.get_value("llama_cpp.model.logits_all", False),
            vocab_only=config.get_value("llama_cpp.model.vocab_only", False),
            use_mmap=config.get_value("llama_cpp.model.use_mmap", True),
            use_mlock=config.get_value("llama_cpp.model.use_mlock", False),
            embedding=config.get_value("llama_cpp.model.embedding", True),
            n_threads=config.get_value("llama_cpp.model.n_threads", None),
            last_n_tokens_size=config.get_value(
                "llama_cpp.model.last_n_tokens_size", 64
            ),
            lora_base=config.get_value("llama_cpp.model.lora_base", None),
            lora_path=config.get_value("llama_cpp.model.lora_path", None),
            tensor_split=config.get_value("llama_cpp.model.tensor_split", None),
            rope_freq_base=config.get_value("llama_cpp.model.rope_freq_base", 10000.0),
            rope_freq_scale=config.get_value("llama_cpp.model.rope_freq_scale", 1.0),
        )

    def _download_model(self) -> str:
        """
        Download the model file if not already present in the cache.

        Returns:
            str: The path to the downloaded model file.
        """
        logging.info(f"Using {self.repo_id} to load {self.filename}")
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                model_path = hf_hub_download(
                    repo_id=self.repo_id,
                    filename=self.filename,
                    cache_dir=self.cache_dir,
                    resume_download=True,
                )
                logging.info(f"Using {model_path} to load {self.filename} into memory")
                return model_path
            except (EntryNotFoundError, RepositoryNotFoundError) as e:
                logging.error(f"Error downloading model: {e}")
                sys.exit(1)
            except LocalEntryNotFoundError as e:
                logging.error(f"Error accessing model: {e}")
                if HfApi().is_online():
                    logging.info("Retrying download...")
                    retries += 1
                else:
                    logging.error("Network is not available. Cannot retry download.")
                    sys.exit(1)
            except Exception as e:
                logging.error(f"Error downloading model: {e}")
                sys.exit(1)

        logging.error("Max retries exceeded. Failed to download the model.")
        sys.exit(1)

    def _stream_chat_completion(
        self, response_generator: Iterator[ChatCompletionChunk]
    ) -> ChatModelChatCompletion:
        """
        Process the stream of chat completion chunks and return the generated message.

        Args:
            response_generator (Iterator[ChatCompletionChunk]): The chat completion chunk stream.

        Returns:
            ChatModelChatCompletion: The generated message.
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

        return ChatModelChatCompletion(role="assistant", content=content)

    def get_completion(self, prompt: str) -> ChatModelTextCompletion:
        """
        Get completions from the Llama language model.

        Raises:
            NotImplementedError: This method is not implemented in the LlamaCppAPI class.
        """
        raise NotImplementedError

    def get_chat_completion(
        self, messages: List[ChatModelChatCompletion]
    ) -> ChatModelChatCompletion:
        """
        Generate chat completions using the Llama language model.

        Args:
            messages (List[ChatModelChatCompletion]): List of chat completion messages.

        Returns:
            ChatModelChatCompletion: The generated chat completion message.

        Raises:
            ValueError: If the 'messages' argument is empty or None.
        """
        if not messages:
            raise ValueError("'messages' argument cannot be empty or None")

        try:
            response = self.model.create_chat_completion(
                messages=messages,
                max_tokens=self.config.get_value(
                    "llama_cpp.chat_completions.max_tokens", 1024
                ),
                temperature=self.config.get_value(
                    "llama_cpp.chat_completions.temperature", 0.8
                ),
                top_p=self.config.get_value("llama_cpp.chat_completions.top_p", 0.95),
                top_k=self.config.get_value("llama_cpp.chat_completions.top_k", 40),
                stream=True,
                stop=self.config.get_value("llama_cpp.chat_completions.stop", []),
                repeat_penalty=self.config.get_value(
                    "llama_cpp.chat_completions.repeat_penalty", 1.1
                ),
            )
            return self._stream_chat_completion(response)
        except Exception as e:
            logging.error(f"Error generating chat completions: {e}")
            return ChatModelChatCompletion(role="system", content=str(e))

    def get_embedding(self, input: Union[str, List[str]]) -> ChatModelEmbedding:
        """
        Generate embeddings using the Llama language model.

        Args:
            input (Union[str, List[str]]): The input string or list of strings.

        Returns:
            ChatModelEmbedding: The generated embedding data.

        Raises:
            ValueError: If the 'input' argument is empty or None.
        """
        if not input:
            raise ValueError("'input' argument cannot be empty or None")

        try:
            embedding: Dict[str, Any] = self.model.create_embedding(input=input)
            sorted_embeddings: List[Dict[str, Any]] = sorted(
                embedding["data"],
                key=lambda e: e["index"],
            )
            # Return Embedding Vectors as List[float]
            return [result["embedding"] for result in sorted_embeddings]
        except Exception as e:
            logging.error(f"Error generating embeddings: {e}")
            return []

    def get_encoding(self, text: str) -> ChatModelEncoding:
        """
        Get the token encoding for a single text using the Llama language model.

        Args:
            text (str): The input text to encode.

        Returns:
            ChatModelEncoding (List[int]): The token encoding for the given text.
        """
        # Convert input text from string to bytes using utf-8 encoding
        text_bytes = text.encode("utf-8")

        # Tokenize the text using the Llama language model
        encoding_tokens = self.model.tokenize(text_bytes)

        return encoding_tokens
