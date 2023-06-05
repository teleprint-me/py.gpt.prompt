# pygptprompt/command/cd.py
import os

from pygptprompt.session.proxy import SessionQueueProxy


class ChangeDirectory:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    def execute(self, command: str) -> str:
        # The command is the first argument.
        args = command.strip().split()

        # The directory path is the second argument
        # Assume a directory path is given
        # If no path is given, then assume local directory
        try:
            directory = args[1].strip()
        except (IndexError,):
            directory = "."

        if not self.queue_proxy.policy.is_accessible(directory):
            return "RoleError: Access denied! You shouldn't snoop in private places."

        if os.path.isfile(directory):
            return f"Error: '{directory}' is a file. Not a directory."

        if not os.path.isdir(directory):
            return f"Error: Directory '{directory}' not found."

        try:
            os.chdir(directory)
            return f"Successfully changed directory to '{directory}'"
        except Exception as e:
            return f"Error changing directory to {directory}: {str(e)}."
