# pygptprompt/context/session.py
import json
import os

from prompt_toolkit import prompt

from pygptprompt.context.chat import ChatContext


def get_session_name() -> str:
    session_name = prompt("Enter a session name: ")
    return session_name


def make_session_directory(chat_context: ChatContext) -> None:
    dir_path = chat_context.config.get_value("path.session", "sessions")
    os.makedirs(dir_path, exist_ok=True)


def load_session(chat_context: ChatContext) -> list[dict[str, str]]:
    session_path = chat_context.config.get_value("path.session", "sessions")
    try:
        with open(f"{session_path}/{chat_context.session_name}.json", "r") as file:
            session_data = json.load(file)
        return session_data
    except FileNotFoundError:
        print(f"SessionError: Session {chat_context.session_name} not found.")
        return []


def save_session(chat_context: ChatContext) -> None:
    session_path = chat_context.config.get_value("path.session", "sessions")
    session_name = chat_context.session_name
    session_data = chat_context.messages
    try:
        with open(f"{session_path}/{session_name}.json", "w") as file:
            json.dump(session_data, file, indent=4)
        print(f"SessionInfo: Session {session_name} saved successfully.")
    except Exception as e:
        print(f"SessionError: Error saving session {session_name}: {str(e)}.")
