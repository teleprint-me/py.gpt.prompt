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
        self.base_limit_percentage: float = config.get_value(
            "chat_completions.base_limit_percentage", 0.1
        )
        self.encoding: Encoding = tiktoken.encoding_for_model(self.model)

    @property
    def upper_limit(self) -> int:
        # Get the token limit for the model from the dictionary, or use the default limit
        token_limit: int = TOKEN_LIMITS.get(self.model, TOKEN_LIMITS["default"])
        upper_limit: int = token_limit - self.max_tokens
        return upper_limit

    @property
    def base_limit(self) -> int:
        # Calculate the base limit as a percentage of the upper limit
        base_limit: int = int(self.upper_limit * self.base_limit_percentage)
        return base_limit

    def get_content_count(self, content: str) -> int:
        return len(self.encoding.encode(content))

    def get_message_count(self, message: dict[str, str]) -> int:
        """Returns the number of tokens in a text string."""
        if "content" in message:
            content: str = message["content"]
        else:
            content: str = ""

        return self.get_content_count(content)

    def get_total_message_count(self, messages: list[dict[str, str]]) -> int:
        """Returns the number of tokens in a text string."""
        total_tokens: int = 0

        for message in messages:
            total_tokens += self.get_message_count(message)

        return total_tokens

    def is_overflow(
        self,
        new_message: dict[str, str],
        messages: list[dict[str, str]],
        token_offset: int = TOKEN_OFFSET,
    ) -> bool:
        new_message_token_count = self.get_message_count(new_message)
        messages_total_token_count = self.get_total_message_count(messages)
        token_count = new_message_token_count + messages_total_token_count
        total_token_count = token_offset + token_count
        return total_token_count >= self.upper_limit
