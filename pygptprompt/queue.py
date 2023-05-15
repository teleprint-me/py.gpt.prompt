from typing import Any, Optional

import tiktoken
from assistant.setting import (
    AssistantPath,
    AssistantSetting,
    force_read_json,
    get_assistant_path,
    write_json,
)
from openai import OpenAI


class MessageQueue:
    """Class for managing conversational context between assistant and user."""

    def __init__(self, assistant_path: Optional[AssistantPath] = None):
        self.path = get_assistant_path(assistant_path)
        self.setting = AssistantSetting(self.path)
        self.completions: list[dict[str, Any]] = []
        self.messages: list[dict[str, str]] = [self.system_message]
        self.history = self.messages[:]
        self.openai = OpenAI()
        self.load()

    def __len__(self) -> int:
        return len(self.messages)

    @property
    def assistant(self) -> str:
        return self.setting.read("assistant")

    @property
    def chat_completions(self) -> dict[str, Any]:
        return self.setting.read("chat_completions")

    @property
    def model(self) -> str:
        return self.chat_completions["model"]

    @property
    def temperature(self) -> float:
        return self.chat_completions["temperature"]

    @property
    def max_tokens(self) -> int:
        return self.chat_completions["max_tokens"]

    @property
    def system_message(self) -> dict[str, str]:
        return self.setting.read_nested("prompt", "system", self.assistant)

    @property
    def token_count(self) -> int:
        conversation_text = " ".join(
            [message["content"] for message in self.messages]
        )
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(conversation_text))

    @property
    def last_message(self) -> dict[str, str]:
        try:
            return self.messages[-1]
        except (IndexError,):
            return {}

    @property
    def overflow(self) -> bool:
        token_offset = 512
        token_count = token_offset + self.token_count
        return token_count >= self.max_tokens

    def add_message(self, role: str, content: str) -> None:
        self.dequeue_messages()
        message = {"role": role.strip(), "content": content.strip()}
        if message not in self.messages:
            self.messages.append(message)
        if message not in self.history:
            self.history.append(message)

    def remove_message(self, index: int = 1) -> dict[str, str]:
        if len(self) > 2:
            return self.messages.pop(index)
        return {}

    def dequeue_messages(self) -> list[dict[str, str]]:
        dequeue = []
        while len(self) > 2 and self.overflow:
            dequeue.append(self.remove_message(1))
        return dequeue

    def extend(self, messages: list[dict[str, str]]) -> None:
        """Extend messages within the given context."""
        for message in messages:
            if message not in self.messages:
                self.messages.append(message)
            if message not in self.history:
                self.history.append(message)

    def generate_completion(self) -> str:
        response = self.openai.completion.chat_completions(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        self.completions.append(response)

        role = response["choices"][0]["message"]["role"].strip()
        content = response["choices"][0]["message"]["content"].strip()

        self.add_message(role, content)

        return content

    def clear_messages(self) -> None:
        self.messages = [self.system_message]

    def clear_history(self) -> None:
        self.history = self.messages[:]

    def clear_completions(self) -> None:
        self.completions = []

    def clear(self) -> None:
        self.clear_messages()
        self.clear_history()

    def save(self) -> None:
        write_json(self.path.message, self.messages)
        write_json(self.path.history, self.history)
        write_json(self.path.completion, self.completions)

    def load(self) -> None:
        self.messages = force_read_json(self.path.message, self.messages)
        self.history = force_read_json(self.path.history, self.history)
        self.completions = force_read_json(
            self.path.completion, self.completions
        )
