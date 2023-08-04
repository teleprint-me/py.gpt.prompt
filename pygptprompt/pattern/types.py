"""
pygptprompt/pattern/types.py
"""
from abc import abstractmethod
from typing import List, Literal, NotRequired, Protocol, TypedDict

ChatModelTextCompletion = str
ChatModelEncoding = List[int]
ChatModelEmbedding = List[float]
ChatModelDocument = str
ChatModelDocuments = List[ChatModelDocument]


class ChatCompletionMessage(TypedDict):
    """
    Base chat completion message class.

    Attributes:
        role (Literal["assistant", "user", "system"]): The role of the message.
        content (str): The content of the message.
        user (Optional[str]): The user associated with the message (optional).
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
        function_call (Optional[str]): The function call associated with the message (optional).
        function_args (Optional[str]): The function arguments associated with the message (optional).
        user (Optional[str]): The user associated with the message (optional).
    """

    role: Literal["assistant", "user", "system", "function"]
    content: NotRequired[str]
    function_call: NotRequired[str]
    function_args: NotRequired[str]
    user: NotRequired[str]


class EmbeddingFunction(Protocol):
    @abstractmethod
    def __call__(self, texts: ChatModelDocuments) -> ChatModelEmbedding:
        """
        An abstract method defining the embedding function's call signature.

        Args:
            texts (List[str]): A list of text documents.

        Returns:
            List[float]: The resulting embedding for the given text documents.
        """
        raise NotImplementedError
