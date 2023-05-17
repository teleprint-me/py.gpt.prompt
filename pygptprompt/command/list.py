import os

from pygptprompt.config import get_config
from pygptprompt.policy import is_accessible

__config__ = get_config()


def get_file_info(file_path: str) -> str:
    is_dir = os.path.isdir(file_path)
    if is_dir:
        file_size = "-"
    else:
        file_size = os.path.getsize(file_path)

    type_info = "dir" if is_dir else "file"
    return f"{file_path:30} {type_info:10} {file_size}"


def list_directory(command: str) -> str:
    allowed_paths = [] if not __config__ else __config__["allowed_paths"]
    denied_paths = [] if not __config__ else __config__["denied_paths"]

    # The command is the first argument.
    args = command.split()[1:]

    # The directory path is the second argument
    directory = args[0].strip()

    if not is_accessible(directory, allowed_paths, denied_paths):
        return "RoleError: Access denied! You shouldn't snoop in private places."

    if not os.path.isdir(directory):
        return f"Error: Directory '{directory}' not found."

    try:
        files = [
            file
            for file in os.listdir(directory)
            if is_accessible(os.path.join(directory, file), allowed_paths, denied_paths)
        ]
        file_info_list = [
            get_file_info(os.path.join(directory, file)) for file in files
        ]
        return "\n".join(file_info_list)
    except Exception as e:
        return f"Error listing directory {directory}: {str(e)}."
