# pygptprompt/chat/session.py
import json
import os
import string

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygptprompt.chat.interpreter import ChatInterpreter
from pygptprompt.session.model import ChatModel
from pygptprompt.session.policy import ChatPolicy
from pygptprompt.session.token import ChatToken
from pygptprompt.setting import GlobalConfiguration, read_json, write_json


class ChatSession:
    def __init__(self, config: GlobalConfiguration):
        self.config: GlobalConfiguration = config
        self.model: ChatModel = ChatModel(config)
        self.token: ChatToken = ChatToken(config)
        self.policy: ChatPolicy = ChatPolicy(config)
        self.interpreter: ChatInterpreter = ChatInterpreter(self.config, self.token)
        self.transcript: list[dict[str, str]] = [self.model.system_message]
        self.messages: list[dict[str, str]] = [self.model.system_message]
        self.name: str = ""

    @property
    def path(self) -> str:
        return self.config.get_value("path.session", "sessions")

    @property
    def history(self) -> FileHistory:
        return FileHistory(f"{self.path}/history/{self.name}.history")

    def make_directory(self) -> None:
        os.makedirs(self.path, exist_ok=True)
        os.makedirs(f"{self.path}/context", exist_ok=True)
        os.makedirs(f"{self.path}/transcript", exist_ok=True)
        os.makedirs(f"{self.path}/history", exist_ok=True)

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

    def load(self) -> None:
        try:
            self.messages = read_json(f"{self.path}/context/{self.name}.json")
            self.transcript = read_json(f"{self.path}/transcript/{self.name}.json")
            print(f"SessionInfo: Session {self.name} loaded successfully.")
        except FileNotFoundError:
            print(f"SessionError: Session {self.name} not found.")
        except json.JSONDecodeError:
            print(f"SessionError: Error decoding JSON data for session {self.name}.")

    def save(self) -> None:
        try:
            write_json(f"{self.path}/context/{self.name}.json", self.messages)
            write_json(f"{self.path}/transcript/{self.name}.json", self.transcript)
            print(f"SessionInfo: Session {self.name} saved successfully.")
        except PermissionError:
            print(f"SessionError: Permission denied when saving session {self.name}.")
        except json.JSONDecodeError:
            print(f"SessionError: Error encoding JSON data for session {self.name}.")
        except Exception as e:
            print(f"SessionError: Error saving session {self.name}: {str(e)}.")
