# pygptprompt/chat/assistant_interface.py
from pygptprompt.chat.session import ChatSession
from pygptprompt.command.factory import command_factory
from pygptprompt.format import print_bold
from pygptprompt.openai import OpenAI
from pygptprompt.token import truncate_messages_for_token_limit


class AssistantInterface:
    def __init__(self, session: ChatSession):
        self.session: ChatSession = session
        # API Key defaults to `./.env`. (defined in config)
        self.openai: OpenAI = OpenAI(session.config.get_api_key())

    @staticmethod
    def print_assistant_prompt():
        print_bold("assistant")

    @staticmethod
    def print_newline():
        print("\n")  # pad output with newline characters

    @staticmethod
    def is_command(message: str) -> bool:
        return message.startswith("/")

    @staticmethod
    def execute_command(command: str) -> str:
        print()  # pad with a newline to avoid mangling
        command_response = command_factory(command)
        print(command_response)
        return command_response

    @staticmethod
    def append_command_response(message: str, command_response: str) -> str:
        return f"{message}\n{command_response}"

    def get_assistant_message(self):
        return self.openai.stream_chat_completions(
            self.session.messages,
            model=self.session.model.name,
            max_tokens=self.session.model.max_tokens,
            temperature=self.session.model.temperature,
        )

    def add_message_to_conversation(self, message: str):
        self.session.messages = truncate_messages_for_token_limit(
            self.session.messages,
            {"role": "assistant", "content": message},
            self.session.model.upper_limit,
            self.session.model.encoding,
        )

    def prompt_gpt(self) -> None:
        self.print_assistant_prompt()
        assistant_message = self.get_assistant_message()

        if assistant_message:
            assistant_content = assistant_message["content"]
            if self.is_command(assistant_content):
                command_response = self.execute_command(assistant_content)
                assistant_content = self.append_command_response(
                    assistant_content, command_response
                )
                assistant_message = {"role": "assistant", "content": assistant_content}

            self.add_message_to_conversation(assistant_message)

        self.print_newline()
