# pygptprompt/session.py
import json
import os
from typing import Optional

from prompt_toolkit import prompt


def get_session_name() -> str:
    session_name = prompt("Enter a name for the session: ")
    return session_name


def create_directory(dir_path: Optional[str] = None) -> None:
    dir_path = dir_path if dir_path else "sessions"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def load_session(session_name: str) -> list[dict[str, str]]:
    try:
        with open(f"sessions/{session_name}.json", "r") as file:
            session_data = json.load(file)
        return session_data
    except FileNotFoundError:
        print(f"SessionError: Session {session_name} not found.")
        return []


def save_session(
    session_name: str,
    session_data: list[dict[str, str]],
) -> None:
    try:
        with open(f"sessions/{session_name}.json", "w") as file:
            json.dump(session_data, file, indent=4)
        print(f"SessionInfo: Session {session_name} saved successfully.")
    except Exception as e:
        print(f"SessionError: Error saving session {session_name}: {str(e)}.")


def delete_session(session_name: str) -> None:
    try:
        os.remove(f"sessions/{session_name}.json")
        print(f"SessionInfo: Session {session_name} deleted successfully.")
    except FileNotFoundError:
        print(f"SessionError: Session {session_name} not found.")
    except Exception as e:
        print(f"SessionError: Error deleting session {session_name}: {str(e)}.")
