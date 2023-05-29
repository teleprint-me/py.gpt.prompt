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
    def write_result_to_file(command_result: str) -> str:
        # TODO: Implement write_result_to_file method
        # Save the result to a file in storage/dirname/filename
        # Filename could be a UUID.
        file_information = "File information"
        return file_information

    @staticmethod
    def extract_code_blocks(message: str) -> list[str]:
        # TODO: Implement extract_code_blocks method
        # Extract file extensions from a block (e.g. ```py\nprint("Hello, World!")\n```)
        # `py` would be used for the file extension to cache the source
        return re.split(r"(```[^`]*```)", message)

    def is_result_too_large(self, command_result: str) -> bool:
        # TODO: Refine this check to ensure context window won't overflow
        # This check should consider token count in addition to string length.
        return len(command_result) > self.queue_proxy.token.upper_limit

    def execute_command(self, line: str) -> str:
        return command_factory(self.queue_proxy, line)

    def replace_line_with_result(self, line: str, command_result: str) -> str:
        if self.is_result_too_large(command_result):
            command_result = self.write_result_to_file(command_result)
        # NOTE: User needs to see result
        print(f"\n```\n{command_result.strip()}\n```")  # NOTE: Leave this line here!
        return f"{line}\n```\n{command_result.strip()}\n```"

    def interpret_message(self, message_content: str) -> str:
        lines: list[str] = message_content.split("\n")
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
