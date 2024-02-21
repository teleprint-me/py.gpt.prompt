"""
pygptprompt/model/base.py
"""
from abc import ABC, abstractmethod
from typing import (
    List,
    Literal,
    NotRequired,
    Protocol,
    Required,
    TypedDict,
    TypeVar,
    Union,
)

import numpy as np

# Represents a vector in the chat model,
# which could be either a list of integers or floats.
ChatModelVector = Union[List[int], List[float]]

# Alias for a vector encoding in the chat model.
ChatModelEncoding = ChatModelVector

# Represents an embedding as a list of ChatModelVectors.
ChatModelEmbedding = List[ChatModelVector]

# Represents a document or string in the chat model.
ChatModelDocument = str

# Represents a list of documents or strings in the chat model.
ChatModelDocuments = List[ChatModelDocument]

# Represents a text completion in the chat model.
ChatModelTextCompletion = str

# Include the new types for Images
# Images is a list of Image objects
Image = Union[np.uint, np.int_, np.float_]
Images = List[Image]

# Define a Generic type for EmbeddingFunction
Embeddable = Union[ChatModelDocuments, Images]
D = TypeVar("D", bound=Union[ChatModelDocuments, Images])


class DeltaContent(TypedDict, total=False):
    """
    Represents the delta content which may contain either actual content or a function call.

    Attributes:
        - content: The text content.
        - function_call: Information about a function call.
    """

    content: NotRequired[str]
    function_call: NotRequired[str]


class FunctionCall(TypedDict):
    """
    Represents the function call which may contain an optional JSON Schema representing arguments.

    Attributes:
        - name: The name of the function to be called.
        - arguments: Optional JSON Schema representing arguments to be passed to the function call.
    """

    name: Required[str]
    arguments: NotRequired[str]


class ChatCompletionMessage(TypedDict):
    """

    Attributes:
        - role: The role of the message (either 'assistant', 'user', or 'system').
        - content: The content of the message.
        - user: The user who originated this message, if applicable.
    """

    role: Literal["assistant", "user", "system"]
    content: Required[str]
    user: NotRequired[str]


class ChatModelResponse(ChatCompletionMessage):
    """
    Represents a single completion message from the chat model.

    Attributes:
        - role: The role of the message. It can be 'assistant', 'user', 'system', or 'function'.
        - content: The content of the message.
        - function_call: The function being called, if applicable.
        - function_args: The arguments for the function call, if applicable.
        - name: The name of the function, if applicable.
        - user: The user who originated this message, if applicable.
    """

    role: Literal["assistant", "user", "system", "function"]
    content: NotRequired[str]
    function_call: NotRequired[FunctionCall]
    name: NotRequired[str]
    user: NotRequired[str]


class ChatModel(ABC):
    """
    Abstract base class for a ChatModel.

    Attributes:
        config (ConfigurationManager): The configuration template for the model.
    """

    @abstractmethod
    def __init__(self, config: object):
        """
        Constructor method for ChatModel.

        Args:
            config (ConfigurationManager): The configuration template for the model.
        """
        raise NotImplementedError

    @abstractmethod
    def get_completion(self, prompt: str) -> ChatModelTextCompletion:
        """
        Get a single text completion for a given prompt.

        Args:
            prompt (str): The input prompt for generating the completion.

        Returns:
            ChatModelTextCompletion (str): The text completion.

        NOTE:
            Completions will be deprecated according to the OpenAI API documentation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_chat_completion(
        self, messages: List[ChatModelResponse]
    ) -> ChatModelResponse:
        """
        Get a text completion for a conversation based on the provided messages.

        Args:
            messages (List[ChatModelResponse]): The list of ChatModelResponse objects representing the conversation.

        Returns:
            ChatModelResponse (Dict[LiteralString, str]): The text completion for the conversation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_embedding(self, input: Union[str, List[str]]) -> ChatModelEmbedding:
        """
        Get the embedding for a given input.

        Args:
            input (Union[str, List[str]]): The input text or list of texts to get embeddings for.

        Returns:
            ChatModelEmbedding (List[List[float]]): The embedding representation of the input.
        """
        raise NotImplementedError

    @abstractmethod
    def get_encoding(self, text: str) -> ChatModelEncoding:
        """
        Get the encoding for a single text.

        Args:
            text (str): The string of text to encode.

        Returns:
            ChatModelEncoding (List[int]): The encoding for the text.
        """
        raise NotImplementedError


class EmbeddingFunction(Protocol[D]):
    @abstractmethod
    def __call__(self, texts: ChatModelDocuments) -> ChatModelEmbedding:
        """
        An abstract method defining the embedding function's call signature.

        Args:
            texts (List[str]): A list of text documents.

        Returns:
            ChatModelEmbedding (List[List[float]]): The resulting embedding for the given text documents.
        """
        raise NotImplementedError
