import os
import subprocess

from pygptprompt.config import get_config

__config__ = get_config()


def list_directory(command: str) -> str:
    directory = command.replace("/ls", "").strip()
    if not os.path.isdir(directory):
        return f"Error: Directory {directory} not found."

    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing directory {directory}: {str(e)}."


def run_subprocess(command: str) -> str:
    command_to_run = command.replace("/subprocess", "").strip()
    args = command_to_run.split(" ")

    try:
        process = subprocess.run(args, check=True, text=True, capture_output=True)
        return process.stdout
    except subprocess.CalledProcessError as e:
        return (
            f"Command '{' '.join(args)}' returned non-zero exit status {e.returncode}."
        )
