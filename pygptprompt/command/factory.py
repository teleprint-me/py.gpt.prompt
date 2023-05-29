# pygptprompt/command/factory.py
from pygptprompt.command.feed import RSSHandler
from pygptprompt.command.help import HelpDisplay
from pygptprompt.command.list import ListDirectory
from pygptprompt.command.process import SubprocessRunner
from pygptprompt.command.read import ReadFile
from pygptprompt.command.web import RobotsFetcher, WebsiteFetcher
from pygptprompt.session.proxy import SessionQueueProxy

COMMAND_MAP = {
    "/": SubprocessRunner,
    "/ls": ListDirectory,
    "/browse": WebsiteFetcher,
    "/robots": RobotsFetcher,
    "/rss": RSSHandler,
    "/help": HelpDisplay,
    "/read": ReadFile,
}


def command_factory(
    session_proxy: SessionQueueProxy,
    command: str,
) -> str:
    for command_prefix, Handler in COMMAND_MAP.items():
        if command == command_prefix or command.startswith(command_prefix + " "):
            handler = Handler(session_proxy)
            return handler.execute(command)

    # If no specific command matches, treat it as a subprocess command
    return COMMAND_MAP["/"](session_proxy).execute(command)
