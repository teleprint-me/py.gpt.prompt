"""
pygptprompt/model/openai.py

"Embrace the journey of discovery and evolution in the world of software development, and remember that adaptability is key to staying resilient in the face of change."
    - OpenAI's GPT-3.5
"""
import sys
from typing import Any, Dict, Iterator, List, Tuple, Union

import openai
from llama_cpp import ChatCompletionChunk
from tiktoken import Encoding, encoding_for_model

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.base import (
    ChatModel,
    ChatModelEmbedding,
    ChatModelEncoding,
    ChatModelResponse,
    ChatModelTextCompletion,
    DeltaContent,
    FunctionCall,
)


class OpenAIModel(ChatModel):
    """
    ChatModel class for interacting with the OpenAI language models.

    Args:
        config (ConfigurationManager): The configuration manager instance.

    Attributes:
        config (ConfigurationManager): The configuration manager instance.
    """

    def __init__(self, config: ConfigurationManager):
        """
        Initialize the OpenAIAPI class.

        Args:
            config (ConfigurationManager): The configuration manager instance.
        """
        self.config = config
        self.logger = config.get_logger("general", self.__class__.__name__)
        self.client = openai.OpenAI(
            api_key=config.get_environment(),
        )

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
        # print(delta)
        if delta and delta.content:
            token = delta.content
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

        # NOTE: Keep an eye on this.
        # function_call may have properties and produce
        # `ERROR:OpenAIModel:Error generating chat completions: 'function_call' object is not subscriptable`
        if delta and delta.function_call:
            function_call = delta.function_call
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
                    role="assistant",
                    content=None,
                    function_call=FunctionCall(
                        name=function_call_name,
                        arguments=function_call_args,
                    ),
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

            delta = chunk.choices[0].delta
            content = self._extract_content(delta, content)
            function_call_name, function_call_args = self._extract_function_call(
                delta, function_call_name, function_call_args
            )

            self.logger.debug(f"Extracted delta: {delta}")
            self.logger.debug(f"Current content: {content}")
            self.logger.debug(
                f"Current function_call_name: {function_call_name}, function_call_args: {function_call_args}"
            )

            finish_reason = chunk.choices[0].finish_reason
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

        # NOTE: The finish reason should be present.
        # If the finish reason vanishes, then something unexpected happened.
        self.logger.debug(f"Generated content: {content}")
        self.logger.debug("Exiting _stream_chat_completion without a finish_reason.")
        # NOTE: There is no message, but content is always generated.
        # Return the generated content even though no finish reason was given.
        return ChatModelResponse(role="assistant", content=content)

    def get_completion(self, prompt: str) -> ChatModelTextCompletion:
        """
        Get completions from the OpenAI language models.

        Raises:
            NotImplementedError: This method is not implemented in the OpenAIAPI class.
        """
        raise NotImplementedError

    def get_chat_completion(
        self,
        messages: List[ChatModelResponse],
    ) -> ChatModelResponse:
        """
        Generate chat completions using the OpenAI language models.

        Args:
            messages (List[ChatModelResponse]): The list of chat completion messages.

        Returns:
            ChatModelResponse (Dict[LiteralString, str]): The model's response as a message.

        Raises:
            ValueError: If `messages` argument is empty or `None`.
        """
        if not messages:
            raise ValueError("'messages' argument cannot be empty or None")

        try:
            # Call the OpenAI API's /v1/chat/completions endpoint
            response = self.client.chat.completions.create(
                messages=messages,
                functions=self.config.get_value("function.definitions", []),
                function_call=self.config.get_value("function.call", "auto"),
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
            self.logger.error(f"Error generating chat completions: {e}")
            return ChatModelResponse(role="assistant", content=str(e))

    def get_embedding(self, input: Union[str, List[str]]) -> ChatModelEmbedding:
        """
        Generate embeddings using the OpenAI language models.

        Args:
            input (Union[str, List[str]]): The input text or list of texts to generate embeddings for.

        Returns:
            ChatModelEmbedding (List[List[float]]): The generated embedding vector.

        Raises:
            ValueError: If the 'input' argument is empty or None.
        """
        if not input:
            raise ValueError("'input' argument cannot be empty or None")

        try:
            # Call the OpenAI API's /v1/embeddings endpoint
            embedding: Dict[str, Any] = self.client.embeddings.create(
                input=input,
                model=self.config.get_value(
                    "openai.embedding.model", "text-embedding-ada-002"
                ),
            )
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
        Get the token encoding for a single text using the OpenAI language model.

        Args:
            text (str): The input text to encode.

        Returns:
            ChatModelEncoding (List[int]): The token encoding for the given text.

        Raises:
            ValueError: If the 'text' argument is empty or None.
        """
        if not text:
            raise ValueError("'text' argument cannot be empty or None")

        encoding: Encoding = encoding_for_model(
            model_name=self.config.get_value(
                "openai.chat_completions.model", "gpt-3.5-turbo"
            )
        )

        return encoding.encode(text=text)
