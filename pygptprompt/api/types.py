"""
pygptprompt/api/types.py
"""

from typing import Literal, NotRequired, Optional

from llama_cpp import ChatCompletionMessage


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
