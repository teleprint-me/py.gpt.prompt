"""
pygptprompt/api/types.py
"""

from typing import Literal, NotRequired, Union

from llama_cpp import ChatCompletionMessage

from pygptprompt.api.llama_cpp import LlamaCppAPI
from pygptprompt.api.openai import OpenAIAPI

ChatModel = Union[OpenAIAPI, LlamaCppAPI]


class ExtendedChatCompletionMessage(ChatCompletionMessage):
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
