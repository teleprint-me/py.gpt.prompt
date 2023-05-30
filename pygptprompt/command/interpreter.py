# pygptprompt/command/interpreter.py
import re

from pygptprompt.command.factory import command_factory
from pygptprompt.session.proxy import SessionQueueProxy


class CommandInterpreter:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    @staticmethod
    def is_command(line: str) -> bool:
        return line.strip().startswith("/")

    @staticmethod
    def is_in_quotes(line: str) -> bool:
        return line.strip().startswith(("'", '"'))

    @staticmethod
    def is_in_backticks(line: str) -> bool:
        return line.strip().startswith(("`", "```", "````"))

    @staticmethod
    def extract_code_blocks(message: str) -> list[str]:
        # TODO: Implement extract_code_blocks method
        # Extract file extensions from a block (e.g. ```py\nprint("Hello, World!")\n```)
        # `py` would be used for the file extension to cache the source
        return re.split(r"(```[^`]*```)", message)

    def execute_command(self, line: str) -> str:
        return command_factory(self.queue_proxy, line)

    def replace_line_with_result(self, line: str, command_result: str) -> str:
        # NOTE: User needs to see result
        padded_result = f"\n```\n{command_result.strip()}\n```"
        print(padded_result)  # NOTE: Leave this line here!
        return f"{line}\n{padded_result}\n"

    def interpret_message(self, message_content: str) -> str:
        lines: list[str] = message_content.strip().split("\n")
        in_code_block: bool = False
        for i, line in enumerate(lines):
            if line.strip() == "```":
                in_code_block = not in_code_block
            if in_code_block:
                continue
            if (
                self.is_command(line)
                and not self.is_in_quotes(line)
                and not self.is_in_backticks(line)
            ):
                command_result = self.execute_command(line)
                lines[i] = self.replace_line_with_result(line, command_result)
        return "\n".join(lines)
