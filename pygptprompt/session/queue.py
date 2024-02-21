"""
"Simple is better than complex. Complex is better than complicated."
    - Tim Peters

- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2465602/

pygptprompt/session/queue.py
"""
import os
import string
from json import JSONDecodeError
from typing import Optional

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygptprompt.api.openai import OpenAI
from pygptprompt.config.json import force_read_json, write_json
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.session.model import SessionModel
from pygptprompt.session.policy import SessionPolicy
from pygptprompt.session.token import SessionToken


class SessionQueue:
    """Class for managing conversational context between assistant and user."""

    def __init__(self, provider, config_path: Optional[str] = None):
        # ConfigurationManager defaults to `./config.json`
        self.config: ConfigurationManager = ConfigurationManager(config_path)
        # A class for handling the model details
        # NOTE: We'll need to restructure this class, but it should
        # represent the current model that used for the given session.
        # We should be able to get details such as it's system prompt,
        # max tokens it can generate, it's maximum sequence length,
        # and the amount of space reserved for additional tokens such
        # as content injection from a command or function call.
        self.model: SessionModel = SessionModel(self.config)
        # A class for handling tokens using tiktoken
        # NOTE: This is straightforward and self descriptive. We'll need
        # to modify it accordingly adjusting our approach for handling
        # the model factory instead.
        self.token: SessionToken = SessionToken(self.config)
        # A class for handling User Access Controls
        # NOTE: This is a bit more complex, but handles the user and model
        # permissions, e.g. What directories are we allowed to traverse?
        self.policy: SessionPolicy = SessionPolicy(self.config)
        # Transcript represents the entire conversation in completion
        self.transcript: list[dict[str, str]] = [self.model.system_message]
        # Messages represents the models context window
        self.messages: list[dict[str, str]] = [self.model.system_message]
        # Custom OpenAI interface; see `pygptprompt/openai` for more info
        # NOTE: This should be replaced by the model factory as it handles
        # this for us and has now be abstracted away removing the responsibility
        # from this class.
        self.openai: OpenAI = OpenAI(self.config.get_api_key())
        # User defined session name; user is prompted for input
        self.name: str = ""

    def __len__(self) -> int:
        return len(self.messages)

    @property
    def path(self) -> str:
        return self.config.get_value("path.session", "sessions")

    @property
    def last_message(self) -> dict[str, str]:
        try:
            return self.messages[-1]
        except (IndexError,):
            return self.model.system_message

    @property
    def last_role(self) -> str:
        return self.last_message.get("role", "system")

    @property
    def last_content(self) -> str:
        return self.last_message.get("content", "You are a helpful assistant.")

    @property
    def history(self) -> FileHistory:
        return FileHistory(f"{self.path}/{self.name}/prompt.history")

    def set_name(self) -> None:
        allowed_chars = set(string.ascii_letters + string.digits + ".-_")
        while True:
            try:
                self.name = prompt("Enter a session name: ")
                if not self.name:
                    print("SessionError: Session name cannot be empty.")
                elif not set(self.name).issubset(allowed_chars):
                    print(
                        "SessionError: Session name can only contain alphanumeric characters, periods, hyphens, and underscores."
                    )
                else:
                    break
            except (KeyboardInterrupt, EOFError):
                print("SessionInfo: Session Aborted.")
                exit()

    def pop_message(self, index: int = 1) -> dict[str, str]:
        if len(self) > 2:
            return self.messages.pop(index)
        return {}

    def dequeue(self, message: dict[str, str]) -> list[dict[str, str]]:
        dequeue = []
        while len(self) > 2 and self.token.is_overflow(message, self.messages):
            dequeue.append(self.pop_message(1))
        return dequeue

    def enqueue(self, role: str, content: str) -> None:
        message = {"role": role.strip(), "content": content.strip()}
        self.dequeue(message)
        if message not in self.messages:
            self.messages.append(message)
        if message not in self.transcript:
            self.transcript.append(message)

    def extend(self, messages: list[dict[str, str]]) -> None:
        """Extend messages within the given context."""
        for message in messages:
            if message not in self.messages:
                self.messages.append(message)
            if message not in self.transcript:
                self.transcript.append(message)

    def stream_completion(self) -> str:
        message = self.openai.completions.stream_chat_completions(
            messages=self.messages,
            model=self.model.name,
            max_tokens=self.model.max_tokens,
            temperature=self.model.temperature,
        )

        alt_content = "SessionQueueError: Oops! Something unexpected went wrong!"
        return message.get("content", alt_content)

    def clear_messages(self) -> None:
        self.messages = [self.model.system_message]

    def clear_transcript(self) -> None:
        self.transcript = self.messages[:]

    def clear(self) -> None:
        self.clear_messages()
        self.clear_transcript()

    def make_directory(self) -> None:
        os.makedirs(f"{self.path}/{self.name}", exist_ok=True)

    def save(self) -> None:
        # NOTE: Always guarantee the configured path exists
        self.make_directory()

        try:
            write_json(f"{self.path}/{self.name}/context.json", self.messages)
            write_json(f"{self.path}/{self.name}/transcript.json", self.transcript)
            print(f"SessionInfo: Session {self.name} saved successfully.")
        except PermissionError:
            print(f"SessionError: Permission denied when saving session {self.name}.")
        except JSONDecodeError:
            print(f"SessionError: Error encoding JSON data for session {self.name}.")
        except Exception as e:
            print(f"SessionError: Error saving session {self.name}: {str(e)}.")

    def load(self) -> None:
        # NOTE: Always guarantee the configured path exists
        self.make_directory()

        try:
            # `force_read_json` creates the file if it doesn't exist
            # this is ideal for non-existent sessions
            self.messages = force_read_json(
                f"{self.path}/{self.name}/context.json", self.messages
            )
            self.transcript = force_read_json(
                f"{self.path}/{self.name}/transcript.json", self.transcript
            )
            print(f"SessionInfo: Session {self.name} loaded successfully.")
        except FileNotFoundError:
            print(f"SessionError: Session {self.name} not found.")
        except JSONDecodeError:
            print(f"SessionError: Error decoding JSON data for session {self.name}.")
