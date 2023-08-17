"""
pygptprompt/pattern/model.py
"""
from abc import ABC, abstractmethod
from typing import List, Literal, NotRequired, Protocol, TypedDict, Union

ChatModelVector = Union[List[int], List[float]]
ChatModelEncoding = ChatModelVector
ChatModelEmbedding = List[ChatModelVector]
ChatModelDocument = str
ChatModelDocuments = List[ChatModelDocument]
ChatModelTextCompletion = str


class ChatCompletionMessage(TypedDict):
    """
    Base chat completion message class.

    Attributes:
        role (Literal["assistant", "user", "system"]): The role of the message.
        content (str): The content of the message.
        user (NotRequired[str]): The user associated with the message (optional).
    """

    role: Literal["assistant", "user", "system"]
    content: str
    user: NotRequired[str]


class ChatModelChatCompletion(ChatCompletionMessage):
    """
    Extended chat completion message with additional role options.

    Inherits:
        ChatCompletionMessage: Base chat completion message class.

    Attributes:
        role (Literal["assistant", "user", "system", "function"]): The role of the message.
        content (str): The content of the message.
        function_call (NotRequired[str]): The function call associated with the message (optional).
        function_args (NotRequired[str]): The function arguments associated with the message (optional).
        user (NotRequired[str]): The user associated with the message (optional).
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
        self, messages: List[ChatModelChatCompletion]
    ) -> ChatModelChatCompletion:
        """
        Get a text completion for a conversation based on the provided messages.

        Args:
            messages (List[ChatModelChatCompletion]): The list of ChatModelChatCompletion objects representing the conversation.

        Returns:
            ChatModelChatCompletion (Dict[LiteralString, str]): The text completion for the conversation.
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
