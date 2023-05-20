# pygptprompt/policy.py
import os

from pygptprompt.context.config import get_configuration

__config__ = get_configuration()


def is_traversable(path: str) -> bool:
    """Check if the filepath is valid."""
    return os.path.isabs(path) or os.path.exists(path)


def is_accessible(path: str) -> bool:
    """Check if the filepath is allowed according to the configuration."""
    path = os.path.abspath(path)
    file_access = __config__.get("command_execution", {}).get("file_access", {})
    denied_paths = file_access.get("disallowed_paths", [])
    allowed_paths = file_access.get("allowed_paths", [])

    for denied_path in denied_paths:
        if path.startswith(os.path.abspath(denied_path)):
            return False
    for allowed_path in allowed_paths:
        if path.startswith(os.path.abspath(allowed_path)):
            return True
    return False


def is_command_allowed(command) -> tuple[bool, str]:
    """Check if the command is allowed according to the configuration."""
    shell_config = __config__.get("command_execution", {}).get("shell", {})
    allowed_commands = shell_config.get("allowed_commands", [])
    disallowed_commands = shell_config.get("disallowed_commands", [])
    disallowed_strings = shell_config.get("disallowed_strings", [])
    disallowed_chars = shell_config.get("disallowed_chars", [])

    # Check if the command is explicitly allowed
    if command.split()[0] in allowed_commands:
        return True, ""

    # Check if the command is explicitly disallowed
    if command.split()[0] in disallowed_commands:
        return False, f"Command {command.split()[0]} is explicitly disallowed."

    # Check if the command contains a disallowed string
    for string in disallowed_strings:
        if string in command:
            return False, f"Command contains disallowed string: {string}"

    # Check if the command contains a disallowed character
    for char in disallowed_chars:
        if char in command:
            return False, f"Command contains disallowed character: {char}"

    # If none of the disallowed conditions are met, allow the command
    return True, "No issues"
