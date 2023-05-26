# pygptprompt/command/interpreter.py
import re

from pygptprompt.command.factory import command_factory
from pygptprompt.session.policy import SessionPolicy
from pygptprompt.session.token import SessionToken
from pygptprompt.setting.config import GlobalConfiguration


class CommandInterpreter:
    def __init__(
        self,
        config: GlobalConfiguration,
        policy: SessionPolicy,
        token: SessionToken,
    ):
        self.config: GlobalConfiguration = config
        self.policy: SessionPolicy = policy
        self.token: SessionToken = token

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
        return len(command_result) > self.token.upper_limit

    def replace_line_with_result(self, line: str, command_result: str) -> str:
        if self.is_result_too_large(command_result):
            command_result = self.write_result_to_file(command_result)
        return f"{line}\n{command_result}"

    def execute_command(self, line: str) -> str:
        result = command_factory(self.config, self.policy, line)
        # NOTE: User needs to see result
        print(result)  # NOTE: Leave this line here!
        return result

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
