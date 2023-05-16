import os

from pygptprompt.config import get_config
from pygptprompt.policy import is_accessible

__config__ = get_config()


def read_file(command: str) -> str:
    allowed_paths = [] if not __config__ else __config__["allowed_paths"]
    denied_paths = [] if not __config__ else __config__["denied_paths"]

    # The command is the first argument.
    args = command.split()[1:]

    # The filepath is the second argument
    filepath = args[0]

    if not is_accessible(filepath, allowed_paths, denied_paths):
        return "RoleError: Access denied! You shouldn't snoop in private places."

    if not os.path.isfile(filepath):
        return f"Error: Filepath '{filepath}' not found."

    # Optional starting line number
    start_line = (
        0 if len(args) < 2 else int(args[1]) - 1
    )  # -1 to account for 0-indexing

    # Optional ending line number
    end_line = None if len(args) < 3 else int(args[2])

    if end_line is not None and end_line <= start_line:
        return "Error: Ending line number must be greater than starting line number."

    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            if end_line is None:
                return "".join(lines[start_line:])
            else:
                return "".join(lines[start_line:end_line])
    except Exception as e:
        return f"Error reading file {filepath}: {str(e)}."
