# pygptprompt/command/read.py
import json
import os
from typing import Optional

from pygptprompt.session.proxy import SessionQueueProxy
from pygptprompt.setting.json import dump_json


class ReadFile:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    def get_file_content(
        self,
        filepath: str,
        start_line: int,
        end_line: Optional[int] = None,
    ) -> str:
        if filepath.endswith(".json"):
            with open(filepath, "r") as file:
                lines = json.dumps(json.load(file), indent=4).split("\n")
                content = self.join_lines(lines, start_line, end_line, "\n")
        else:  # Treat as a plaintext file
            with open(filepath, "r") as f:
                lines = f.readlines()
                content = self.join_lines(lines, start_line, end_line)
        return content

    def join_lines(
        self,
        lines: list[str],
        start_line: int,
        end_line: Optional[int] = None,
        seperator: Optional[str] = None,
    ) -> str:
        seperator = seperator if seperator else ""
        if end_line is None:
            content = seperator.join(lines[start_line:])
        else:
            content = seperator.join(lines[start_line:end_line])

        return content

    def execute(self, command: str) -> str:
        # The command is the first argument.
        args = command.split()[1:]

        if not args:
            return "ReadError: No file path specified."

        # The filepath is the second argument
        filepath = args[0]

        if not self.queue_proxy.policy.is_accessible(filepath):
            return f"AccessError: Access to file {filepath} is not allowed."

        if not os.path.isfile(filepath):
            return f"ReadError: Filepath '{filepath}' not found."

        try:
            # Optional starting line number
            # NOTE: -1 to account for 0-indexing
            start_line = 0 if len(args) < 2 else int(args[1]) - 1
        except ValueError:
            return "ReadError: <start_line> must be an integer."

        try:
            # Optional ending line number
            end_line = None if len(args) < 3 else int(args[2])
        except ValueError:
            return "ReadError: <end_line> must be an integer."

        if end_line is not None and end_line <= start_line:
            return "ReadError: Ending line number must be greater than starting line number."

        try:
            content = self.get_file_content(filepath, start_line, end_line)
            return self.queue_proxy.handle_content_size(content, filepath)
        except Exception as e:
            return f"ReadError: Error reading file {filepath}: {str(e)}."
