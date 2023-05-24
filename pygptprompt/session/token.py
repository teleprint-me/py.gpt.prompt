# pygptprompt/session/token.py
import tiktoken
from tiktoken import Encoding

from pygptprompt.setting.config import GlobalConfiguration

# Define a dictionary for token limits
TOKEN_LIMITS = {
    "gpt-3.5-turbo": 4096,
    "gpt-4": 8192,
    "default": 2048,
}
TOKEN_OFFSET = 512


class SessionToken:
    def __init__(self, config: GlobalConfiguration):
        self.model: str = config.get_value("chat_completions.model", "gpt-3.5-turbo")
        self.max_tokens: int = config.get_value("chat_completions.max_tokens", 1024)
        self.encoding: Encoding = tiktoken.encoding_for_model(self.model)

    @property
    def upper_limit(self) -> int:
        # Get the token limit for the model from the dictionary, or use the default limit
        token_limit: int = TOKEN_LIMITS.get(self.model, TOKEN_LIMITS["default"])
        upper_limit: int = token_limit - self.max_tokens
        return upper_limit

    def is_message_within_limit(self, message_token_count: int) -> bool:
        return message_token_count <= self.upper_limit

    def get_token_count(self, message: dict[str, str]) -> int:
        """Returns the number of tokens in a text string."""
        if "content" in message:
            content: str = message["content"]
        else:
            content: str = ""

        return len(self.encoding.encode(content))

    def get_total_token_count(self, messages: list[dict[str, str]]) -> int:
        """Returns the number of tokens in a text string."""
        total_tokens: int = 0

        for message in messages:
            if "content" in message:
                content: str = message["content"]
                total_tokens += len(self.encoding.encode(content))

        return total_tokens

    def is_context_overflow(
        self,
        messages: list[dict[str, str]],
        token_offset: int = TOKEN_OFFSET,
    ) -> bool:
        token_count = token_offset + self.get_total_token_count(messages)
        return token_count >= self.upper_limit

    def can_enqueue(
        self,
        messages: list[dict[str, str]],
        new_message: dict[str, str],
        token_offset: int = TOKEN_OFFSET,
    ) -> bool:
        # Calculate the token count for the new message
        new_message_token_count: int = self.get_token_count([new_message])

        # If the new message is too long to fit into the context window,
        # print an error and return False
        if not self.is_message_within_limit(new_message_token_count):
            print(
                f"MessageError: Message too long ({new_message_token_count} tokens). Maximum is {self.upper_limit} tokens."
            )
            return False

        # Calculate the total token count for the current messages
        total_token_count: int = self.get_total_token_count(messages)

        # Calculate token overflow
        token_overflow: int = total_token_count + new_message_token_count + token_offset

        # If the total token count plus the new message's token count plus the offset is within the limit,
        # return True, else return False
        return token_overflow <= self.upper_limit

    def print_token_count(self, message: dict[str, str]) -> None:
        # Calculate the total number of tokens enqueued
        token_count: int = self.get_token_count(message)
        # Output updated token count
        print(f"Message consumed {token_count} tokens.\n")

    def print_total_token_count(self, messages: list[dict[str, str]]) -> None:
        # Calculate the total number of tokens enqueued
        total_token_count: int = self.get_total_token_count(messages)
        # Output updated token count
        print(f"Context window consumed {total_token_count} tokens.\n")
