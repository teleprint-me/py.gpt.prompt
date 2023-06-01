# pygptprompt/command/process.py
import os
import shlex
import subprocess
from uuid import uuid4

from pygptprompt.command.webtools import write_to_cache
from pygptprompt.session.proxy import SessionQueueProxy


class SubprocessRunner:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    def _get_cache_path(self, command: str) -> str:
        # Get the storage path
        storage_path = self.queue_proxy.config.get_value("path.storage", "storage")

        # Generate a uniquely identifiable file name
        file_name = f"{command}-{str(uuid4())[:6]}.log"

        # Create a path for the cache
        cache_path = os.path.join(storage_path, "shell", file_name)

        return cache_path

    def execute(self, command: str) -> str:
        """Run a subprocess command and return its output."""
        command = command.lstrip("/")
        args = shlex.split(command)

        # Check if the command is allowed
        allowed, message = self.queue_proxy.policy.is_command_allowed(command)
        if not allowed:
            return f"CommandError: {message}"

        # Check if the file paths in the command are accessible
        for arg in args:
            if self.queue_proxy.policy.is_traversable(arg):
                if not self.queue_proxy.policy.is_accessible(arg):
                    return f"AccessError: Access to file {arg} is not allowed."

        # Run the command
        try:
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                check=True,
                shell=False,  # NOTE: Enabling this is potentially dangerous!
            )
            cache_path = self._get_cache_path(args[0])
            write_to_cache(cache_path, result.stdout)
            return self.queue_proxy.handle_content_size(result.stdout, cache_path)
        except subprocess.CalledProcessError as e:
            return f"CommandError: Command '{command}' returned non-zero exit status {e.returncode}."
