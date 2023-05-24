# pygptprompt/chat/context.py
from typing import Any, Optional

from pygptprompt.chat.assistant import AssistantInterface

# from pygptprompt.chat.interpreter import ChatInterpreter
from pygptprompt.chat.session import ChatSession
from pygptprompt.chat.user import UserInterface
from pygptprompt.format import print_bold
from pygptprompt.session.token import ChatToken
from pygptprompt.setting.config import GlobalConfiguration


class ChatQueue:
    def __init__(self, config_path: Optional[str] = None):
        # GlobalConfiguration defaults to `./config.json` (defined in config)
        self.config: GlobalConfiguration = GlobalConfiguration(config_path)
        # Session defaults to `./sessions` (defined in config)
        self.session: ChatSession = ChatSession(self.config)
        self.token: ChatToken = self.session.token
        self.user: UserInterface = UserInterface(self.session)
        self.assistant: AssistantInterface = AssistantInterface(self.session)

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
            self.token.print_token_count(self.session.messages)

            # Handle user input
            if self.user.prompt():
                continue

            # Prompt model - Call custom streaming API
            self.assistant.prompt()

            # Save the updated messages to the session file
            self.session.save()
