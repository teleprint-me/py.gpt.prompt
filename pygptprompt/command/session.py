# pygptprompt/command/session.py
import json
import os

from pygptprompt.setting.config import GlobalConfiguration


class SessionHandler:
    def __init__(self, config: GlobalConfiguration):
        self.config = config
        self.session_path = self.config.get_value("path.session", "sessions")
        self.create_directory()

    def create_directory(self):
        if not os.path.exists(self.session_path):
            os.makedirs(self.session_path)

    def load_session(self, session_name: str) -> dict:
        try:
            with open(f"{self.session_path}/{session_name}.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_session(self, session_name: str, session_data: dict) -> None:
        with open(f"{self.session_path}/{session_name}.json", "w") as f:
            json.dump(session_data, f)

    def delete_session(self, session_name: str) -> str:
        try:
            os.remove(f"{self.session_path}/{session_name}.json")
            return f"SessionInfo: Session {session_name} deleted successfully."
        except FileNotFoundError:
            return f"SessionError: Session {session_name} not found."
        except Exception as e:
            return f"SessionError: Error deleting session {session_name}: {str(e)}."

    def handle_session_command(self, command: str) -> str:
        args = command.split()
        if len(args) < 3:
            return "Session command requires an action and a label. Try /session create|load|save|delete <label>."

        action = args[1]
        label = args[2]

        if action == "create":
            if self.load_session(label):
                return f"Session {label} already exists. Use /session load {label} to load the session."
            self.save_session(label, {})
            return f"Session {label} created successfully."

        elif action == "load":
            if not self.load_session(label):
                return f"Session {label} not found."
            return f"Session {label} loaded successfully."

        elif action == "save":
            if not self.load_session(label):
                return f"Session {label} not found."
            self.save_session(
                label, {}
            )  # save_session needs the data to be saved. You need to decide where it comes from.
            return f"Session {label} saved successfully."

        elif action == "delete":
            return self.delete_session(label)

        else:
            return (
                "Invalid session command. Try /session create|load|save|delete <label>."
            )
