# pygptprompt/chat/interpreter.py
import re

from pygptprompt.chat.model import ChatModel
from pygptprompt.command.factory import command_factory


class ChatInterpreter:
    def __init__(self, model: ChatModel):
        self.model = model

    def interpret_message(self, message: str) -> str:
        blocks = self.extract_code_blocks(message)
        for i, block in enumerate(blocks):
            if not self.is_in_quotes(block) and not self.is_in_backticks(block):
                lines = block.split("\n")
                for j, line in enumerate(lines):
                    if self.is_command(line):
                        command_result = self.execute_command(line)
                        lines[j] = self.replace_line_with_result(line, command_result)
                blocks[i] = "\n".join(lines)
        return "\n".join(blocks)

    @staticmethod
    def is_command(line: str) -> bool:
        return line.strip().startswith("/")

    @staticmethod
    def execute_command(line: str) -> str:
        return command_factory(line)

    def replace_line_with_result(self, line: str, command_result: str) -> str:
        if self.is_result_too_large(command_result):
            command_result = self.write_result_to_file(command_result)
        return f"{line}\n{command_result}"

    def is_result_too_large(self, command_result: str) -> bool:
        return len(command_result) > self.model.upper_limit

    @staticmethod
    def write_result_to_file(command_result: str) -> str:
        # This is a placeholder for your actual implementation
        file_information = "File information"
        return file_information

    @staticmethod
    def is_in_quotes(line: str) -> bool:
        return line.strip().startswith(("'", '"'))

    @staticmethod
    def is_in_backticks(line: str) -> bool:
        return line.strip().startswith("`")

    @staticmethod
    def extract_code_blocks(message: str) -> list[str]:
        return re.split(r"(```[^`]*```)", message)
