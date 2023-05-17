import shlex
import subprocess


def run_git_command(command: str) -> str:
    args = shlex.split(command)

    # Check that the command starts with /git
    if args[0] != "/git":
        return "Error: Invalid Git command format."

    git_args = args[1:]
    try:
        result = subprocess.run(
            ["git"] + git_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
