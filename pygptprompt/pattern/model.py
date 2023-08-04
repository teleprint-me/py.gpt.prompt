"""
pygptprompt/pattern/model.py
"""
from abc import ABC, abstractmethod
from typing import List, Literal, NotRequired, Union

from llama_cpp import ChatCompletionMessage

from pygptprompt.pattern.mapping import MappingTemplate

ChatModelTextCompletion = str
ChatModelEmbedding = List[float]
ChatModelEncoding = List[int]


class ChatModelChatCompletion(ChatCompletionMessage):
    """
    Extended chat completion message with additional role options.

    Inherits:
        ChatCompletionMessage: Base chat completion message class.

    Attributes:
        role (Literal["assistant", "user", "system", "function"]): The role of the message.
        content (str): The content of the message.
        user (Optional[str]): The user associated with the message (optional).
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
        config (MappingTemplate): The configuration template for the model.
    """

    @abstractmethod
    def __init__(self, config: MappingTemplate):
        """
        Constructor method for ChatModel.

        Args:
            config (MappingTemplate): The configuration template for the model.
        """
        raise NotImplementedError

    @abstractmethod
    def get_completion(self, prompt: str) -> ChatModelTextCompletion:
        """
        Get a single text completion for a given prompt.

        Args:
            prompt (str): The input prompt for generating the completion.

        Returns:
            ChatModelTextCompletion: The text completion.

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
            ChatModelChatCompletion: The text completion for the conversation.
        """
        raise NotImplementedError

    @abstractmethod
    def get_embedding(self, input: Union[str, List[str]]) -> ChatModelEmbedding:
        """
        Get the embedding for a given input.

        Args:
            input (Union[str, List[str]]): The input text or list of texts to get embeddings for.

        Returns:
            ChatModelEmbedding: The embedding representation of the input.
        """
        raise NotImplementedError

    @abstractmethod
    def get_encoding(self, text: str) -> ChatModelEncoding:
        """
        Get the encoding for a single text.

        Args:
            text (str): The string of text to encode.

        Returns:
            ChatModelEncoding: The encoding for the text.
        """
        raise NotImplementedError
