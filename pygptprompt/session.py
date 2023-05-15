import os

from prompt_toolkit import prompt


def create_sessions_directory():
    if not os.path.exists("sessions"):
        os.makedirs("sessions")


def name_session():
    session_name = prompt("Enter a name for the session: ")
    return session_name


def read_session(session_name):
    try:
        with open(f"sessions/{session_name}.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: Session {session_name} not found."


def save_session(session_name, session_data):
    try:
        with open(f"sessions/{session_name}.txt", "w") as file:
            file.write(session_data)
        return f"Session {session_name} saved successfully."
    except Exception as e:
        return f"Error saving session {session_name}: {str(e)}."


def delete_session(session_name):
    try:
        os.remove(f"sessions/{session_name}.txt")
        return f"Session {session_name} deleted successfully."
    except FileNotFoundError:
        return f"Error: Session {session_name} not found."
    except Exception as e:
        return f"Error deleting session {session_name}: {str(e)}"
