# pygptprompt/chat/session.py
import json
import os
import string

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygptprompt.chat.model import ChatModel
from pygptprompt.chat.policy import ChatPolicy
from pygptprompt.config import Configuration
from pygptprompt.token import get_token_count


class ChatSession:
    def __init__(self, config: Configuration):
        self.config: Configuration = config
        self.model: ChatModel = ChatModel(config)
        self.policy: ChatPolicy = ChatPolicy(config)
        self.messages: list[dict[str, str]] = [self.model.system_message]
        self.name: str = ""

    @property
    def path(self) -> str:
        return self.config.get_value("path.session", "sessions")

    @property
    def history(self) -> FileHistory:
        return FileHistory(f"{self.path}/{self.name}.history")

    def set_name(self) -> None:
        allowed_chars = set(string.ascii_letters + string.digits + ".-_")
        while True:
            self.name = prompt("Enter a session name: ")
            if not self.name:
                print("Error: Session name cannot be empty.")
            elif not set(self.name).issubset(allowed_chars):
                print(
                    "Error: Session name can only contain alphanumeric characters, periods, hyphens, and underscores."
                )
            else:
                break

    def print_token_count(self) -> None:
        # Calculate the total number of tokens enqueued
        token_count: int = get_token_count(
            self.model.encoding.name, messages=self.messages
        )

        # Output updated token count
        print(f"Consumed {token_count} tokens.\n")

    def make_directory(self) -> None:
        os.makedirs(self.path, exist_ok=True)

    def load(self) -> None:
        try:
            with open(f"{self.path}/{self.name}.json", "r") as file:
                self.messages = json.load(file)
            print(f"SessionInfo: Session {self.name} loaded successfully.")
        except FileNotFoundError:
            print(f"SessionError: Session {self.name} not found.")
        except json.JSONDecodeError:
            print(f"SessionError: Error decoding JSON data for session {self.name}.")

    def save(self) -> None:
        try:
            with open(f"{self.path}/{self.name}.json", "w") as file:
                json.dump(self.messages, file, indent=4)
            print(f"SessionInfo: Session {self.name} saved successfully.")
        except PermissionError:
            print(f"SessionError: Permission denied when saving session {self.name}.")
        except json.JSONDecodeError:
            print(f"SessionError: Error encoding JSON data for session {self.name}.")
        except Exception as e:
            print(f"SessionError: Error saving session {self.name}: {str(e)}.")
