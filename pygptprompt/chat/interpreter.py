# pygptprompt/chat/interpreter.py
import re

from pygptprompt.session.token import ChatToken

# from pygptprompt.command.factory import command_factory
from pygptprompt.setting.config import GlobalConfiguration


class ChatInterpreter:
    def __init__(self, config: GlobalConfiguration, token: ChatToken):
        self.config: GlobalConfiguration = config
        self.token: ChatToken = token

    @staticmethod
    def is_command(line: str) -> bool:
        return line.strip().startswith("/")

    @staticmethod
    def is_in_quotes(line: str) -> bool:
        return line.strip().startswith(("'", '"'))

    @staticmethod
    def is_in_backticks(line: str) -> bool:
        return line.strip().startswith("`")

    @staticmethod
    def write_result_to_file(command_result: str) -> str:
        # This is a placeholder for your actual implementation
        file_information = "File information"
        return file_information

    @staticmethod
    def extract_code_blocks(message: str) -> list[str]:
        return re.split(r"(```[^`]*```)", message)

    def is_result_too_large(self, command_result: str) -> bool:
        return len(command_result) > self.token.upper_limit

    def replace_line_with_result(self, line: str, command_result: str) -> str:
        if self.is_result_too_large(command_result):
            command_result = self.write_result_to_file(command_result)
        return f"{line}\n{command_result}"

    def execute_command(self, line: str) -> str:
        # return command_factory(self.config, line)
        return ""  # NOTE: Temporary placeholder until chat is fixed

    def interpret_message(self, message_content: str) -> str:
        lines = message_content.split("\n")
        for i, temp in enumerate(lines):
            line = temp.strip()
            is_command = self.is_command(line)
            not_in_quotes = not self.is_in_quotes(line)
            not_in_ticks = not self.is_in_backticks(line)
            if is_command and not_in_quotes and not_in_ticks:
                command_result = self.execute_command(line)
                lines[i] = self.replace_line_with_result(line, command_result)
        return "\n".join(lines)
