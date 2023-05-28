# pygptprompt/command/read.py
import os

from pygptprompt.session.policy import SessionPolicy
from pygptprompt.setting.config import GlobalConfiguration


class ReadFile:
    def __init__(self, config: GlobalConfiguration, policy: SessionPolicy):
        self.config: GlobalConfiguration = config
        self.policy: SessionPolicy = policy

    def execute(self, command: str) -> str:
        # The command is the first argument.
        args = command.split()[1:]

        if not args:
            return "Error: No file path specified."

        # The filepath is the second argument
        filepath = args[0]

        if not self.policy.is_accessible(filepath):
            return "RoleError: Access denied! You shouldn't snoop in private places."

        if not os.path.isfile(filepath):
            return f"Error: Filepath '{filepath}' not found."

        try:
            # Optional starting line number
            # NOTE: -1 to account for 0-indexing
            start_line = 0 if len(args) < 2 else int(args[1]) - 1
        except ValueError:
            return "Error: <start_line> must be an integer."

        try:
            # Optional ending line number
            end_line = None if len(args) < 3 else int(args[2])
        except ValueError:
            return "Error: <end_line> must be an integer."

        if end_line is not None and end_line <= start_line:
            return (
                "Error: Ending line number must be greater than starting line number."
            )

        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
                if end_line is None:
                    return "".join(lines[start_line:])
                else:
                    return "".join(lines[start_line:end_line])
        except Exception as e:
            return f"Error reading file {filepath}: {str(e)}."
