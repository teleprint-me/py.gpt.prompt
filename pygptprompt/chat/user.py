# pygptprompt/chat/user_interface.py
import prompt_toolkit

from pygptprompt.chat.model import ChatModel
from pygptprompt.chat.session import ChatSession
from pygptprompt.command.factory import command_factory
from pygptprompt.format import print_bold
from pygptprompt.token import truncate_messages_for_token_limit


class UserInterface:
    def __init__(self, session: ChatSession):
        self.session: ChatSession = session
        self.model: ChatModel = session.model

    @staticmethod
    def prompt_continuation(width, line_number, is_soft_wrap):
        return ">" * width

    @staticmethod
    def is_command(message: str) -> bool:
        return message.startswith("/")

    @staticmethod
    def execute_command(command: str) -> str:
        return command_factory(command)

    @staticmethod
    def append_command_response(message: str, command_response: str) -> str:
        return f"{message}\n{command_response}"

    def handle_interrupt(self):
        self.session.save()
        exit()

    def prompt_user(self) -> bool:
        user_message = self.get_user_input()
        if not user_message:
            return True

        if self.is_command(user_message):
            command_response = self.execute_command(user_message)
            user_message = self.append_command_response(user_message, command_response)

        self.add_message_to_conversation(user_message)
        return False

    def get_user_input(self) -> str:
        try:
            print_bold("user")
            return prompt_toolkit.prompt(
                "> ",
                multiline=True,
                prompt_continuation=self.prompt_continuation,
                history=self.session.history,
            )
        except (KeyboardInterrupt, EOFError):
            self.handle_interrupt()

    def add_message_to_conversation(self, message: str) -> None:
        self.session.messages = truncate_messages_for_token_limit(
            self.session.messages,
            {"role": "user", "content": message},
            self.model.upper_limit,
            self.model.encoding,
        )
        print()
