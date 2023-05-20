# pygptprompt/command/session.py
from pygptprompt.context.session import (
    create_directory,
    create_session,
    delete_session,
    load_session,
    save_session,
)


def handle_session_command(command: str) -> str:
    args = command.split()
    if len(args) < 3:
        return "Session command requires an action and a label. Try /session create|load|save|delete <label>."

    command = args[0]
    action = args[1]
    label = args[2]

    create_directory()

    if action == "create":
        return create_session(label)
    elif action == "load":
        return load_session(label)
    elif action == "save":
        return save_session(label)
    elif action == "delete":
        return delete_session(label)
    else:
        return "Invalid session command. Try /session create|load|save|delete <label>."
