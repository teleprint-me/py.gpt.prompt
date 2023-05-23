# pygptprompt/chat/model.py
import tiktoken

from pygptprompt.config import Configuration
from pygptprompt.singleton import Singleton
from pygptprompt.token import get_token_limit

DEFAULT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": "Your name is ChatGPT. You are a programming assistant. Execute /help for more information. Execute a command when asked to do so. Always respect the users machine.",
}


class ChatModel(Singleton):
    def __init__(self, config: Configuration):
        self.config: Configuration = config

    @property
    def name(self) -> str:
        return self.config.get_value("chat_completions.model", "gpt-3.5-turbo")

    @property
    def max_tokens(self) -> int:
        return self.config.get_value("chat_completions.max_tokens", 1024)

    @property
    def temperature(self) -> float:
        return self.config.get_value("chat_completions.temperature", 0.5)

    @property
    def system_message(self) -> dict[str, str]:
        return self.config.get_value(
            "chat_completions.system_message", DEFAULT_SYSTEM_MESSAGE
        )

    @property
    def encoding(self) -> tiktoken.Encoding:
        return tiktoken.encoding_for_model(self.name)

    @property
    def upper_limit(self) -> int:
        # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
        # gpt-4 context window: `upper_limit = 8192 - max_tokens`
        return get_token_limit(self.name, self.max_tokens)
