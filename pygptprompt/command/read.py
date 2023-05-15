import os

from pygptprompt.config import get_config

__config__ = get_config()


def read_file(command: str) -> str:
    args = command.replace("/read", "").strip().split(" ")

    # First argument is the filename
    filename = args[0]
    if not os.path.isfile(filename):
        return f"Error: File {filename} not found."

    abs_path = os.path.abspath(filename)

    # Get allowed and denied paths from the configuration
    allowed_paths = [] if not __config__ else __config__["allowed_paths"]
    denied_paths = [] if not __config__ else __config__["denied_paths"]

    if any(abs_path.startswith(path) for path in denied_paths):
        return "RoleError: Accessed denied! You shouldn't snoop in private places."

    if not any(abs_path.startswith(path) for path in allowed_paths):
        return "RoleError: Accessed denied! You shouldn't snoop in private places."

    # Optional starting line number
    start_line = (
        0 if len(args) < 2 else int(args[1]) - 1
    )  # -1 to account for 0-indexing

    # Optional ending line number
    end_line = None if len(args) < 3 else int(args[2])

    if end_line is not None and end_line <= start_line:
        return "Error: Ending line number must be greater than starting line number."

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            if end_line is None:
                return "".join(lines[start_line:])
            else:
                return "".join(lines[start_line:end_line])
    except Exception as e:
        return f"Error reading file {filename}: {str(e)}."
