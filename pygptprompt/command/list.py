# pygptprompt/command/list.py
import os

from pygptprompt.session.proxy import SessionQueueProxy


class ListDirectory:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

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

    def get_accessible_files(self, directory: str) -> list:
        files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if self.queue_proxy.policy.is_accessible(file_path):
                files.append(file)
        return files

    def get_file_info_list(self, files: list, directory: str) -> list:
        file_info_list = []
        for file in files:
            file_path = os.path.join(directory, file)
            file_info = self.get_file_info(file_path)
            file_info_list.append(file_info)
        return file_info_list

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

        if not self.queue_proxy.policy.is_accessible(directory):
            return "RoleError: Access denied! You shouldn't snoop in private places."

        if not os.path.isdir(directory):
            return f"Error: Directory '{directory}' not found."

        try:
            header = f"{'File Path':30} {'Type Info':10} {'File Size in Bytes'}\n"

            files = self.get_accessible_files(directory)
            file_info_list = self.get_file_info_list(files, directory)

            body = "\n".join(file_info_list)
            return header + body
        except Exception as e:
            return f"Error listing directory {directory}: {str(e)}."
