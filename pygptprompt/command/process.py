# pygptprompt/command/process.py
import shlex
import subprocess

from pygptprompt.session.proxy import SessionQueueProxy


class SubprocessRunner:
    def __init__(self, session_proxy: SessionQueueProxy):
        self.session_proxy = session_proxy

    def execute(self, command: str) -> str:
        """Run a subprocess command and return its output."""
        command = command.lstrip("/")
        args = shlex.split(command)

        # Check if the command is allowed
        allowed, message = self.session_proxy.policy.is_command_allowed(command)
        if not allowed:
            return f"CommandError: {message}"

        # Check if the file paths in the command are accessible
        for arg in args:
            if self.session_proxy.policy.is_traversable(arg):
                if not self.session_proxy.policy.is_accessible(arg):
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
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"CommandError: Command '{command}' returned non-zero exit status {e.returncode}."
