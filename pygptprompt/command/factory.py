from pygptprompt.command.feed import handle_rss_command
from pygptprompt.command.git import run_git_command
from pygptprompt.command.help import display_help
from pygptprompt.command.list import list_directory
from pygptprompt.command.read import read_file
from pygptprompt.command.tree import display_tree
from pygptprompt.command.web import fetch_and_store_website, fetch_robots_txt


def command_factory(command: str) -> str:
    if command.startswith("/read"):
        content = read_file(command)
    elif command.startswith("/ls"):
        content = list_directory(command)
    elif command.startswith("/tree"):
        content = display_tree(command)
    elif command.startswith("/git"):
        content = run_git_command(command)
    elif command.startswith("/browse"):
        content = fetch_and_store_website(command)
    elif command.startswith("/robots"):
        content = fetch_robots_txt(command)
    elif command.startswith("/rss"):
        content = handle_rss_command(command)
    elif command.startswith("/help"):
        content = display_help(command)
    else:
        content = "Command not recognized."

    return content
