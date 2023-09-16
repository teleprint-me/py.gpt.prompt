"""
pygptprompt/pattern/model.py
"""

from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Literal,
    NotRequired,
    Optional,
    Protocol,
    TypedDict,
    Union,
)

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


class DeltaContent(TypedDict, total=False):
    """
    Represents the delta content which may contain either actual content or a function call.

    Attributes:
        - content (str): The text content.
        - function_call (Optional[Dict[str, Any]]): Information about a function call.
    """

    content: str
    function_call: Optional[Dict[str, Any]]


class ChatCompletionMessage(TypedDict):
    """
    Represents a single completion message from the chat model.

    Attributes:
        - role (Literal): The role of the message (either 'assistant', 'user', or 'system').
        - content (str): The content of the message.
        - user (NotRequired[str]): The user who originated this message, if applicable.
    """

    role: Literal["assistant", "user", "system"]
    content: str
    user: NotRequired[str]


class ChatModelResponse(ChatCompletionMessage):
    """
    Extends ChatCompletionMessage to include optional function calls and their arguments.

    Attributes:
        - role (Literal): The role of the message. It can be 'assistant', 'user', 'system', or 'function'.
        - content (NotRequired[str]): The content of the message.
        - function_call (NotRequired[str]): The function being called, if applicable.
        - function_args (NotRequired[str]): The arguments for the function call, if applicable.
        - user (NotRequired[str]): The user who originated this message, if applicable.
    """

    role: Literal["assistant", "user", "system", "function"]
    content: NotRequired[str]
    function_call: NotRequired[str]
    function_args: NotRequired[str]
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


class EmbeddingFunction(Protocol):
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


class ChatModelEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model: ChatModel):
        """
        Initialize the ChatModelEmbeddingFunction.

        Args:
            model (ChatModel): The chat model instance, e.g. OpenAIModel or LlamaCppModel API.
        """
        self._model = model

    def __call__(self, texts: ChatModelDocuments) -> ChatModelEmbedding:
        """
        Generate embeddings using the chat model.

        Args:
            texts (List[str]): The input texts for which embeddings need to be generated.

        Returns:
            ChatModelEmbedding (List[List[float]]): The list of embeddings generated by the chat model.
        """
        # Replace newlines, which can negatively affect performance.
        texts = [t.replace("\n", " ") for t in texts]

        # Get embeddings from the chat model API
        return self._model.get_embedding(input=texts)
