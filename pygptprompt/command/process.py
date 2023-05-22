# pygptprompt/command/process.py
import shlex
import subprocess

from pygptprompt.context.config import ConfigContext
from pygptprompt.context.policy import is_accessible, is_command_allowed, is_traversable


def run_subprocess(command: str, config: ConfigContext) -> str:
    # First argument is /<command>
    command_to_run = command.lstrip("/")
    # Positional arguments are command_to_run
    args = shlex.split(command_to_run)

    # Check if the command is allowed according to the configuration
    allowed, reason = is_command_allowed(command_to_run, config)
    if not allowed:
        return f"Error: Command not allowed. Reason: {reason}"

    # Check if any argument looks like a file path and is not accessible
    for arg in args[1:]:  # exclude the command itself
        if is_traversable(arg) and not is_accessible(arg, config):
            return f"Error: File path '{arg}' not accessible."

    # Attempt process execution and return result
    try:
        process = subprocess.run(args, check=True, text=True, capture_output=True)
        return process.stdout
    except subprocess.CalledProcessError as e:
        return (
            f"Command '{' '.join(args)}' returned non-zero exit status {e.returncode}."
        )
