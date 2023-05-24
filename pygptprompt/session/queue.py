from typing import Any, Optional

from pygptprompt.openai import OpenAI
from pygptprompt.session.model import SessionModel
from pygptprompt.session.policy import SessionPolicy
from pygptprompt.session.token import SessionToken
from pygptprompt.setting import GlobalConfiguration, force_read_json, write_json


class SessionQueue:
    """Class for managing conversational context between assistant and user."""

    def __init__(self, config_path: Optional[str] = None):
        # GlobalConfiguration defaults to `./config.json` (defined in config)
        self.config: GlobalConfiguration = GlobalConfiguration(config_path)
        # A class for handling the model details
        self.model: SessionModel = SessionModel(self.config)
        # A class for handling tokens using tiktoken
        self.token: SessionToken = SessionToken(self.config)
        # A class for handling User Access Controls
        self.policy: SessionPolicy = SessionPolicy(self.config)
        # Transcript represents the entire conversation in completion
        self.transcript: list[dict[str, str]] = [self.model.system_message]
        # Messages represents the context window
        self.messages: list[dict[str, str]] = [self.model.system_message]
        # Custom OpenAI interface
        self.openai = OpenAI()
        # Load the conversation transcript and context window
        self.load()

    def __len__(self) -> int:
        return len(self.messages)

    @property
    def last_message(self) -> dict[str, str]:
        try:
            return self.messages[-1]
        except (IndexError,):
            return self.model.system_message

    @property
    def last_role(self) -> str:
        return self.last_message.get("role", "")

    @property
    def last_content(self) -> str:
        return self.last_message.get("content", "")

    def add_message(self, role: str, content: str) -> None:
        self.dequeue_messages()
        message = {"role": role.strip(), "content": content.strip()}
        if message not in self.messages:
            self.messages.append(message)
        if message not in self.transcript:
            self.transcript.append(message)

    def remove_message(self, index: int = 1) -> dict[str, str]:
        if len(self) > 2:
            return self.messages.pop(index)
        return {}

    def dequeue_messages(self) -> list[dict[str, str]]:
        dequeue = []
        while len(self) > 2 and self.token.is_context_overflow(self.messages):
            dequeue.append(self.remove_message(1))
        return dequeue

    def extend(self, messages: list[dict[str, str]]) -> None:
        """Extend messages within the given context."""
        for message in messages:
            if message not in self.messages:
                self.messages.append(message)
            if message not in self.transcript:
                self.transcript.append(message)

    def generate_completion(self) -> str:
        message = self.openai.completions.stream_chat_completions(
            messages=self.messages,
            model=self.model.name,
            max_tokens=self.model.max_tokens,
            temperature=self.model.temperature,
        )

        role = message.get("role", "")
        content = message.get("content", "")

        self.add_message(role, content)

        return message["content"]

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
        self.completions = force_read_json(self.path.completion, self.completions)
