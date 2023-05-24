# pygptprompt/chat/user_interface.py
import prompt_toolkit

from pygptprompt.chat.session import ChatSession
from pygptprompt.format import print_bold


class UserInterface:
    def __init__(self, session: ChatSession):
        self.session: ChatSession = session

    # Prompt related methods
    @staticmethod
    def prompt_continuation(width, line_number, is_soft_wrap):
        line_number += 1  # Adjust line_number to start from 1
        spaces = " " * (width - len(str(line_number)))
        return f"{line_number:000}{spaces}"

    def get_user_input(self) -> str:
        try:
            print_bold("user")
            return prompt_toolkit.prompt(
                "1 " + (" " * 3),
                multiline=True,
                prompt_continuation=self.prompt_continuation,
                history=self.session.history,
            )
        except (KeyboardInterrupt, EOFError):
            self.handle_interrupt()

    # Command related methods
    @staticmethod
    def is_command(message: str) -> bool:
        return message.startswith("/")

    def execute_command(self, command: str) -> str:
        # NOTE: Temporary placeholder until chat is fixed
        # return command_factory(self.session.config, command)
        return "Commands are under construction..."

    @staticmethod
    def append_command_response(message: str, command_response: str) -> str:
        print(command_response)
        return f"{message}\n{command_response}"

    # Message handling methods
    def add_message_to_conversation(self, message: str) -> None:
        self.session.messages = self.session.token.enqueue(
            self.session.messages,
            {"role": "user", "content": message},
        )
        self.session.transcript.append(self.session.messages[-1])
        print()

    def handle_interrupt(self):
        self.session.save()
        exit()

    # Main prompt method
    def prompt(self) -> bool:
        user_message = self.get_user_input()

        if not user_message:
            return True

        if self.is_command(user_message):
            command_response = self.execute_command(user_message)
            user_message = self.append_command_response(user_message, command_response)

        self.add_message_to_conversation(user_message)

        return False
