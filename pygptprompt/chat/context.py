# pygptprompt/chat/context.py
from typing import Any, Optional

from pygptprompt.chat.assistant import AssistantInterface
from pygptprompt.chat.interpreter import ChatInterpreter
from pygptprompt.chat.session import ChatSession
from pygptprompt.chat.user import UserInterface
from pygptprompt.config import Configuration
from pygptprompt.format import print_bold


class ChatContext:
    def __init__(self, config_path: Optional[str] = None):
        # Configuration defaults to `./config.json` (defined in config)
        self.config: Configuration = Configuration(config_path)
        # Session defaults to `./sessions` (defined in config)
        self.session: ChatSession = ChatSession(self.config)
        self.interpreter = ChatInterpreter(self.session.model)
        self.user: UserInterface = UserInterface(self.session)
        self.assistant: AssistantInterface = AssistantInterface(self.session)
        # Setup subprocesses for managing I/O
        self.subprocess: dict[str, Any] = {
            "input": "",
            "output": "",
            "original_message": {"role": "", "content": ""},
            "modified_message": {"role": "", "content": ""},
        }

    def setup_session(self) -> None:
        # NOTE: Sessions defaults to `./sessions` (defined in config)
        self.session.make_directory()
        self.session.set_name()  # prompt user for session name
        self.session.load()  # load the session based on given name

    def print_message_history(self) -> None:
        # Print message history
        for message in self.session.messages:
            print()  # Add newline to pad output
            print_bold(message["role"])
            print(message["content"])
        print()  # Add newline to pad output

    def loop(self) -> None:
        self.setup_session()
        self.print_message_history()

        while True:
            self.session.print_token_count()

            # Handle user input
            if self.user.prompt_user():
                continue

            # Prompt model - Call custom streaming API
            self.assistant.prompt_gpt()

            # Save the updated messages to the session file
            self.session.save()
