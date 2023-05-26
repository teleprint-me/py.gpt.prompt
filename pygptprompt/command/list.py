# pygptprompt/command/list.py
import os

from pygptprompt.session.policy import SessionPolicy
from pygptprompt.setting.config import GlobalConfiguration


class ListDirectory:
    def __init__(self, config: GlobalConfiguration, policy: SessionPolicy):
        self.config: GlobalConfiguration = config
        self.policy: SessionPolicy = policy

    @staticmethod
    def get_file_info(file_path: str) -> str:
        # NOTE: This is a helper method for self.execute
        # This method requires a file_path parameter
        is_dir = os.path.isdir(file_path)

        if is_dir:
            file_size = "-"
        else:
            file_size = os.path.getsize(file_path)

        type_info = "dir" if is_dir else "file"

        return f"{file_path:30} {type_info:10} {file_size}"

    def execute(self, command: str) -> str:
        # The command is the first argument.
        args = command.split()[1:]

        # The directory path is the second argument
        # Assume a directory path is given
        # If no path is given, then assume local directory
        try:
            directory = args[0].strip()
        except (IndexError,):
            directory = "."

        if not self.policy.is_accessible(directory):
            return "RoleError: Access denied! You shouldn't snoop in private places."

        if not os.path.isdir(directory):
            return f"Error: Directory '{directory}' not found."

        try:
            header = f"{'File Path':30} {'Type Info':10} {'File Size in Bytes'}\n"
            files = [
                file
                for file in os.listdir(directory)
                if self.policy.is_accessible(os.path.join(directory, file))
            ]
            file_info_list = [
                self.get_file_info(os.path.join(directory, file)) for file in files
            ]
            body = "\n".join(file_info_list)
            return header + body
        except Exception as e:
            return f"Error listing directory {directory}: {str(e)}."
