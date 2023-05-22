# pygptprompt/command/factory.py
from pygptprompt.command.feed import handle_rss_command
from pygptprompt.command.help import display_help
from pygptprompt.command.list import list_directory
from pygptprompt.command.process import run_subprocess
from pygptprompt.command.session import handle_session_command
from pygptprompt.command.web import fetch_and_store_website, fetch_robots_txt
from pygptprompt.context.chat import ChatContext

COMMAND_MAP = {
    "/": run_subprocess,
    "/ls": list_directory,
    "/browse": fetch_and_store_website,
    "/robots": fetch_robots_txt,
    "/rss": handle_rss_command,
    "/session": handle_session_command,
    "/help": display_help,
}


def command_factory(command: str, chat_context: ChatContext) -> str:
    for command_prefix, handler in COMMAND_MAP.items():
        if command == command_prefix or command.startswith(command_prefix + " "):
            return handler(command, chat_context)

    # If no specific command matches, treat it as a subprocess command
    return COMMAND_MAP["/"](command, chat_context)
