# pygptprompt/chat/token.py
import tiktoken
from tiktoken import Encoding

from pygptprompt.config import Configuration

# Define a dictionary for token limits
TOKEN_LIMITS = {
    "gpt-3.5-turbo": 4096,
    "gpt-4": 8192,
    "default": 2048,
}
TOKEN_OFFSET = 512


class ChatToken:
    def __init__(self, config: Configuration):
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

    def get_token_count(self, messages: list[dict[str, str]]) -> int:
        """Returns the number of tokens in a text string."""
        total_tokens: int = 0

        for message in messages:
            if "content" in message:
                content: str = message["content"]
                total_tokens += len(self.encoding.encode(content))

        return total_tokens

    def dequeue(
        self,
        messages: list[dict[str, str]],
        new_message_token_count: int,
        token_offset: int = TOKEN_OFFSET,
    ) -> list[dict[str, str]]:
        # Calculate the total token count for the current messages
        total_token_count: int = self.get_token_count(messages)

        # Calculate token overflow
        token_overflow: int = total_token_count + new_message_token_count + token_offset

        # Remove the oldest messages until the total token count plus the new message's
        # token count plus the offset is within the limit
        while token_overflow > self.upper_limit:
            # Remove the oldest message (after the initial system message)
            try:
                removed_message = messages.pop(1)
            except (IndexError,):
                break  # new message is too large to fit
            total_token_count -= self.get_token_count([removed_message])
            token_overflow = total_token_count + new_message_token_count + token_offset

        return messages

    def enqueue(
        self,
        messages: list[dict[str, str]],
        new_message: dict[str, str],
        token_offset: int = TOKEN_OFFSET,
    ) -> list[dict[str, str]]:
        # Calculate the token count for the new message
        new_message_token_count: int = self.get_token_count([new_message])

        # If the new message is too long to fit into the context window,
        # print an error and return the original messages
        if not self.is_message_within_limit(new_message_token_count):
            print(
                f"MessageError: Message too long ({new_message_token_count} tokens). Maximum is {self.upper_limit} tokens."
            )
            return messages

        # Remove the oldest messages until the total token count plus the new message's
        # token count plus the offset is within the limit
        messages = self.dequeue(messages, new_message_token_count, token_offset)

        # Now that there's enough space, add the new message to the messages list
        messages.append(new_message)

        return messages
