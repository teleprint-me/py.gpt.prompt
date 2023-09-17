"""
pygptprompt/model/llama_cpp.py
"""
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple, Union

from huggingface_hub import hf_hub_download
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)
from llama_cpp import ChatCompletionChunk, Llama

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.model import (
    ChatModel,
    ChatModelEmbedding,
    ChatModelEncoding,
    ChatModelResponse,
    ChatModelTextCompletion,
    DeltaContent,
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
        self.logger = config.get_logger("app.log.general", "LlamaCppModel", "DEBUG")
        self.repo_id = config.get_value(
            "llama_cpp.model.repo_id", "TheBloke/Llama-2-7B-Chat-GGML"
        )
        self.filename = config.get_value(
            "llama_cpp.model.filename", "llama-2-7b-chat.ggmlv3.q5_1.bin"
        )
        self.cache_dir = Path(Path.home(), ".cache", "huggingface", "hub")
        self.model_path = self._discover_model()
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

    def _discover_model(self) -> str:
        """
        Discovers the model path based on configuration or downloads it if necessary.

        Returns:
            str: The path to the model to be used.
        """
        local_model_path = self.config.get_value("llama_cpp.model.local")

        # Check if a local model path is provided and is valid
        if local_model_path:
            if Path(local_model_path).exists():
                self.logger.info(f"Using local model at {local_model_path}")
                return local_model_path
            else:
                self.logger.warning(
                    f"Local model path {local_model_path} does not exist. Falling back to downloading the model."
                )

        # Download the model
        return self._download_model()

    def _download_model(self) -> str:
        """
        Download the model file if not already present in the cache.

        Returns:
            str: The path to the downloaded model file.
        """
        self.logger.info(f"Using {self.repo_id} to load {self.filename}")
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
                self.logger.info(
                    f"Using {model_path} to load {self.filename} into memory"
                )
                return model_path
            except (EntryNotFoundError, RepositoryNotFoundError) as e:
                self.logger.error(f"Error downloading model: {e}")
                sys.exit(1)
            except LocalEntryNotFoundError as e:
                self.logger.error(f"Error accessing model: {e}")
                if HfApi().is_online():
                    self.logger.info("Retrying download...")
                    retries += 1
                else:
                    self.logger.error(
                        "Network is not available. Cannot retry download."
                    )
                    sys.exit(1)
            except Exception as e:
                self.logger.error(f"Error downloading model: {e}")
                sys.exit(1)

        self.logger.error("Max retries exceeded. Failed to download the model.")
        sys.exit(1)

    def _extract_content(self, delta: DeltaContent, content: str) -> str:
        """
        Extracts content from the given delta and appends it to the existing content.

        Args:
            delta (DeltaContent): The delta object containing new content.
            content (str): The existing content.

        Returns:
            str: The updated content after appending the new token.
        """
        self.logger.debug("Entering _extract_content method.")
        self.logger.debug(f"Initial delta: {delta}, content: {content}")

        if delta and "content" in delta and delta["content"]:
            token = delta["content"]
            print(token, end="")
            sys.stdout.flush()
            content += token
        return content

    def _extract_function_call(
        self,
        delta: DeltaContent,
        function_call_name: str,
        function_call_args: str,
    ) -> Tuple[str, str]:
        """
        Extracts function call information from the given delta and updates the function call name and arguments.

        Args:
            delta (DeltaContent): The delta object containing function call information.
            function_call_name (str): The existing function call name.
            function_call_args (str): The existing function call arguments.

        Returns:
            Tuple[str, str]: A tuple containing the updated function call name and arguments.
        """
        self.logger.debug("Entering _extract_function_call method.")
        self.logger.debug(
            f"Initial delta: {delta}, "
            f"function_call_name: {function_call_name}, "
            f"function_call_args: {function_call_args}, "
        )

        if delta and "function_call" in delta and delta["function_call"]:
            function_call = delta["function_call"]
            if not function_call_name:
                function_call_name = function_call.get("name", "")
            function_call_args += str(function_call.get("arguments", ""))
        return function_call_name, function_call_args

    def _handle_finish_reason(
        self,
        finish_reason: str,
        function_call_name: str,
        function_call_args: str,
        content: str,
    ) -> ChatModelResponse:
        """
        Handles the finish reason and returns an ChatModelResponse.

        Args:
            finish_reason (str): The finish reason from the response.
            function_call_name (str): The function call name.
            function_call_args (str): The function call arguments.
            content (str): The generated content.

        Returns:
            ChatModelResponse (Dict[LiteralString, str]): The model's response as a message.
        """
        self.logger.debug("Entering _handle_finish_reason method.")
        self.logger.debug(
            f"Initial finish_reason: {finish_reason}, "
            f"function_call_name: {function_call_name}, "
            f"function_call_args: {function_call_args}, "
            f"content: {content}"
        )

        if finish_reason:
            if finish_reason == "function_call":
                return ChatModelResponse(
                    role="function",
                    function_call=function_call_name,
                    function_args=function_call_args,
                )
            elif finish_reason == "stop":
                print()  # Add newline to model output
                sys.stdout.flush()
                return ChatModelResponse(role="assistant", content=content)
            else:
                # Handle unexpected finish_reason
                raise ValueError(f"Warning: Unexpected finish_reason '{finish_reason}'")

    def _stream_chat_completion(
        self, response_generator: Iterator[ChatCompletionChunk]
    ) -> ChatModelResponse:
        """
        Streams the chat completion response and handles the content and function call information.

        Args:
            response_generator (Iterator[ChatCompletionChunk]): An iterator of ChatCompletionChunk objects.

        Returns:
            ChatModelResponse (Dict[LiteralString, str]): The model's response as a message.
        """
        function_call_name = None
        function_call_args = ""
        content = ""

        self.logger.debug("Entering _stream_chat_completion method.")
        self.logger.debug(
            f"Initial function_call_name: {function_call_name}, function_call_args: {function_call_args}, content: {content}"
        )

        for chunk in response_generator:
            self.logger.debug(f"Processing chunk: {chunk}")

            delta = chunk["choices"][0]["delta"]
            content = self._extract_content(delta, content)
            function_call_name, function_call_args = self._extract_function_call(
                delta, function_call_name, function_call_args
            )

            self.logger.debug(f"Extracted delta: {delta}")
            self.logger.debug(f"Current content: {content}")
            self.logger.debug(
                f"Current function_call_name: {function_call_name}, function_call_args: {function_call_args}"
            )

            finish_reason = chunk["choices"][0]["finish_reason"]
            self.logger.debug(f"Finish reason: {finish_reason}")

            message = self._handle_finish_reason(
                finish_reason,
                function_call_name,
                function_call_args,
                content,
            )

            self.logger.debug(f"Generated message: {message}")

            if message:  # NOTE: Exit early if a finish reason is given.
                self.logger.debug(f"Returning message: {message}")
                return message

        # NOTE: The finish reason should be present, but vanished regardless.
        # The reason for it vanishing is unknown; This is a bug.
        self.logger.debug(f"Generated content: {content}")
        self.logger.debug("Exiting _stream_chat_completion without a finish_reason.")
        # NOTE: There is no message, but content is always generated.
        # Return the generated content even though no finish reason was given.
        return ChatModelResponse(role="assistant", content=content)

    def get_completion(self, prompt: str) -> ChatModelTextCompletion:
        """
        Get completions from the Llama language model.

        Raises:
            NotImplementedError: This method is not implemented in the LlamaCppAPI class.
        """
        raise NotImplementedError

    def get_chat_completion(
        self, messages: List[ChatModelResponse]
    ) -> ChatModelResponse:
        """
        Generate chat completions using the Llama language model.

        Args:
            messages (List[ChatModelResponse]): List of chat completion messages.

        Returns:
            ChatModelResponse (Dict[LiteralString, str]): The model's response as a message.

        Raises:
            ValueError: If the 'messages' argument is empty or None.
        """
        if not messages:
            raise ValueError("'messages' argument cannot be empty or None")

        # NOTE: Larger sequence lengths, or context windows, will delay
        # load times. The load time varies from model to model.
        try:
            response = self.model.create_chat_completion(
                messages=messages,
                functions=self.config.get_value("function.definitions", []),
                function_call=self.config.get_value("function.call", "auto"),
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
            self.logger.error(f"Error generating chat completions: {e}")
            return ChatModelResponse(role="assistant", content=str(e))

    def get_embedding(self, input: Union[str, List[str]]) -> ChatModelEmbedding:
        """
        Generate embeddings using the Llama language model.

        Args:
            input (Union[str, List[str]]): The input string or list of strings.

        Returns:
            ChatModelEmbedding (List[List[float]]): The generated embedding vector.

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
            self.logger.error(f"Error generating embeddings: {e}")
            return []

    def get_encoding(self, text: str) -> ChatModelEncoding:
        """
        Get the token encoding for a single text using the Llama language model.

        Args:
            text (str): The input text to encode.

        Returns:
            ChatModelEncoding (List[int]): The token encoding for the given text.

        Raises:
            ValueError: If the 'text' argument is empty or None.
        """
        if not text:
            raise ValueError("'text' argument cannot be empty or None")

        # Convert input text from string to bytes using utf-8 encoding
        text_bytes = text.encode("utf-8")

        # Tokenize the text using the Llama language model
        encoding_tokens = self.model.tokenize(text_bytes)

        return encoding_tokens
