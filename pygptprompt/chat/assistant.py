# pygptprompt/chat/assistant_interface.py
from pygptprompt.chat.session import ChatSession

# from pygptprompt.command.factory import command_factory
from pygptprompt.format import print_bold
from pygptprompt.openai import OpenAI
from pygptprompt.session.token import ChatToken


class AssistantInterface:
    def __init__(self, session: ChatSession):
        api_key = session.config.get_api_key()
        self.openai: OpenAI = OpenAI(api_key)
        self.token: ChatToken = session.token
        self.session: ChatSession = session

    @staticmethod
    def print_assistant_prompt():
        print_bold("assistant")

    @staticmethod
    def print_newline():
        print("\n")  # pad output with newline characters

    @staticmethod
    def is_command(message: str) -> bool:
        return message.startswith("/")

    def execute_command(self, command: str) -> str:
        # print()  # pad with a newline to avoid mangling
        # command_response = command_factory(self.session.config, command)
        # print(command_response)
        # return command_response
        # NOTE: Temporary placeholder until chat is fixed
        return "Commands are under construction..."

    @staticmethod
    def append_command_response(message: str, command_response: str) -> str:
        print(command_response)
        return f"{message}\n{command_response}"

    def get_assistant_message(self):
        return self.openai.completions.stream_chat_completions(
            self.session.messages,
            model=self.session.model.name,
            max_tokens=self.session.model.max_tokens,
            temperature=self.session.model.temperature,
        )

    def add_message_to_conversation(self, message: str):
        self.session.messages = self.token.enqueue(
            self.session.messages,
            {"role": "assistant", "content": message},
        )
        self.session.transcript.append(self.session.messages[-1])

    def prompt(self) -> None:
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

            self.add_message_to_conversation(assistant_content)

        self.print_newline()
