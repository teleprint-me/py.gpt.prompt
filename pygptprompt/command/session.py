# pygptprompt/command/session.py
import os

from pygptprompt.context.chat import ChatContext
from pygptprompt.context.session import load_session, save_session


def delete_session(session_name: str, chat_context: ChatContext) -> None:
    session_path = chat_context.config.get_value("path.session", "sessions")
    active_session_name = chat_context.session_name

    if session_name == active_session_name:
        print(f"SessionError: Cannot delete the active session {session_name}.")
        return

    try:
        os.remove(f"{session_path}/{session_name}.json")
        print(f"SessionInfo: Session {session_name} deleted successfully.")
    except FileNotFoundError:
        print(f"SessionError: Session {session_name} not found.")
    except Exception as e:
        print(f"SessionError: Error deleting session {session_name}: {str(e)}.")


def handle_session_create(session_name: str, chat_context: ChatContext) -> str:
    session_data = load_session(chat_context)
    if session_data:
        return f"Session {session_name} already exists. Use /session load {session_name} to load the session."

    # Perform any additional setup or initialization for the new session
    # ...

    # Save the new session
    save_session(chat_context)
    return f"Session {session_name} created successfully."


def handle_session_load(session_name: str, chat_context: ChatContext) -> str:
    session_data = load_session(chat_context)
    if not session_data:
        return f"Session {session_name} not found."

    # Perform any additional actions specific to loading a session
    # ...

    return f"Session {session_name} loaded successfully."


def handle_session_save(session_name: str, chat_context: ChatContext) -> str:
    session_data = load_session(chat_context)
    if not session_data:
        return f"Session {session_name} not found."

    # Perform any additional actions specific to saving a session
    # ...

    save_session(chat_context)
    return f"Session {session_name} saved successfully."


def handle_session_delete(session_name: str, config: ConfigContext) -> str:
    delete_session(session_name, config)
    return f"Session {session_name} deleted successfully."


def handle_session_command(command: str, config: ConfigContext) -> str:
    args = command.split()
    if len(args) < 3:
        return "Session command requires an action and a label. Try /session create|load|save|delete <label>."

    command = args[0]
    action = args[1]
    label = args[2]

    create_directory()

    if action == "create":
        return handle_session_create(label, config)
    elif action == "load":
        return handle_session_load(label, config)
    elif action == "save":
        return handle_session_save(label, config)
    elif action == "delete":
        return handle_session_delete(label, config)
    else:
        return "Invalid session command. Try /session create|load|save|delete <label>."
