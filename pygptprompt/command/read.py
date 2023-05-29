# pygptprompt/command/read.py
import os
from typing import Optional

from pygptprompt.session.proxy import SessionQueueProxy


class ReadFile:
    def __init__(self, session_proxy: SessionQueueProxy):
        self.session_proxy = session_proxy

    def get_file_content(
        self,
        filepath: str,
        start_line: int,
        end_line: Optional[int] = None,
    ) -> str:
        with open(filepath, "r") as f:
            lines = f.readlines()
            if end_line is None:
                return "".join(lines[start_line:])
            else:
                return "".join(lines[start_line:end_line])

    def execute(self, command: str) -> str:
        # The command is the first argument.
        args = command.split()[1:]

        if not args:
            return "ReadError: No file path specified."

        # The filepath is the second argument
        filepath = args[0]

        if not self.session_proxy.policy.is_accessible(filepath):
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
            return self.get_file_content(filepath, start_line, end_line)
        except Exception as e:
            return f"ReadError: Error reading file {filepath}: {str(e)}."
