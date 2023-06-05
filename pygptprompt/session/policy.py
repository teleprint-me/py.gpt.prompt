# pygptprompt/session/policy.py
import os

from pygptprompt.pattern.singleton import Singleton
from pygptprompt.setting.config import GlobalConfiguration


class SessionPolicy(Singleton):
    def __init__(self, config: GlobalConfiguration):
        self.config = config

    @staticmethod
    def is_filepath(path: str) -> bool:
        """Check if the filepath is valid."""
        return os.path.isabs(path) or os.path.exists(path)

    @staticmethod
    def is_traversable(path: str) -> bool:
        """Check if the path is a valid directory"""
        return os.path.exists(path) and os.path.isdir(path)

    def is_accessible(self, path: str) -> bool:
        """Check if the filepath is allowed according to the file access configuration."""
        denied_paths = self.config.get_value("access.file.disallowed_paths", [])
        allowed_paths = self.config.get_value("access.file.allowed_paths", [])

        path = os.path.abspath(path)

        for denied_path in denied_paths:
            if path.startswith(os.path.abspath(denied_path)):
                return False
        for allowed_path in allowed_paths:
            if path.startswith(os.path.abspath(allowed_path)):
                return True
        return False

    def is_command_allowed(self, command: str) -> tuple[bool, str]:
        """Check if the command is allowed according to the shell configuration."""
        args = command.strip().split()

        if not args:
            return False, "SessionPolicy: Oops! Something went really wrong!"

        allowed_commands = self.config.get_value("access.shell.allowed_commands", [])
        disallowed_commands = self.config.get_value(
            "access.shell.disallowed_commands", []
        )
        disallowed_strings = self.config.get_value(
            "access.shell.disallowed_strings", []
        )
        disallowed_chars = self.config.get_value("access.shell.disallowed_chars", [])

        # Check if the command is explicitly allowed
        # NOTE: `not` ensures only allowed commands can execute.
        # e.g. `"python" not in ["cat", "ls", "tree"]`.
        # It's easier to specify what's allowed than specify what isn't allowed.
        # In other words, we return False if something is not allowed.
        if args[0] not in allowed_commands:
            return (
                False,
                f"SessionPolicy: Command {args[0]} is not explicitly allowed.",
            )

        # Check if the command is explicitly disallowed
        # NOTE: Disallowed commands are a guardrail, not a guarantee.
        # Warning: This can quickly become unwieldy (You've been warned!).
        if args[0] in disallowed_commands:
            return (
                False,
                f"SessionPolicy: Command {args[0]} is explicitly disallowed.",
            )

        # Check if the command contains a disallowed string
        for string in disallowed_strings:
            if string in command:
                return (
                    False,
                    f"SessionPolicy: Command contains disallowed string: {string}",
                )

        # Check if the command contains a disallowed character
        for char in disallowed_chars:
            if char in command:
                return (
                    False,
                    f"SessionPolicy: Command contains disallowed character: {char}",
                )

        # If none of the disallowed conditions are met, allow the command
        return True, "SessionPolicy: No issues"
