# pygptprompt/command/help.py
from pygptprompt.session.proxy import SessionQueueProxy


class HelpDisplay:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

        self.commands_detail = {
            "/": {
                "info": "Execute shell command",
                "usage": "/<shell_command>",
                "example": "/cat -n pyproject.toml",
                "notes": "All commands are restricted by configuration. `cat`, `cd`, `tree`, and `git` are enabled by default. The user can enable additional commands.",
            },
            "/robots": {
                "info": "Fetch URL's robots.txt.",
                "usage": "/robots <url>",
                "example": "/robots https://www.example.com",
                "notes": "",
            },
            "/browse": {
                "info": "Fetch, markdown-convert, and cache URL's HTML.",
                "usage": "/browse <url>",
                "example": "/browse https://www.example.com",
                "notes": "",
            },
            "/rss": {
                "info": "Display full-text articles from RSS feed.",
                "usage": "/rss <url>",
                "example": "/rss https://www.example.com/rss",
                "notes": "",
            },
            "/cd": {
                "info": "Change current working directory",
                "usage": "/cd <dir>",
                "example": "/cd /path/to/dir",
                "notes": "Access is restricted by configuration. If no directory is specified, it defaults to the current directory.",
            },
            "/ls": {
                "info": "List files in directory",
                "usage": "/ls <dir>",
                "example": "/ls /path/to/dir",
                "notes": "Access is restricted by configuration. If no directory is specified, it defaults to the current directory.",
            },
            "/read": {
                "info": "Read the content of a local file",
                "usage": "/read <file_path> [start_line] [end_line]",
                "example": "/read myfile.txt 5",
                "notes": "Access is restricted by configuration. Line numbers are 1-indexed. Optionally specify the range of lines to read.",
            },
            "/help": {
                "info": "Show help information.",
                "usage": "/help [command]",
                "example": "/help /ls",
                "notes": "If a command is specified, it shows detailed help for that command.",
            },
        }

    def general_help(self) -> str:
        help_text = """
        # Help
        ## Commands:

        **Sub-Process**
        /: Execute shell command (restricted by configuration).

        **Web Pages**
        /robots <url>: Fetch URL's robots.txt.
        /browse <url>: Fetch, markdown-convert, and cache URL's HTML.

        **RSS Feeds**
        /rss <url>: Display full-text articles from RSS feed.

        **Filesystem** (access restricted by configuration)
        /cd <directory>: Change current working directory (defaults to current dir).
        /ls <directory>: List files in directory (defaults to current dir).
        /read <file_path> [start_line] [end_line]: Read the content of a local file.

        **Help**
        /help [command]: Show help information. If a command is specified, it shows detailed help for that command.
        """
        return help_text.strip()

    def detailed_help(self, command: str) -> str:
        if command not in self.commands_detail:
            return f"Error: Unknown command '{command}'. Type '/help' for a list of commands."
        details = self.commands_detail[command]
        detailed_help_text = f"""
        # {command}
        **{details['info']}**
        Usage: `{details['usage']}`
        Example: `{details['example']}`
        Notes: {details['notes']}
        """
        return detailed_help_text.strip()

    def execute(self, command: str) -> str:
        args = command.split()[1:]
        if args:
            return self.detailed_help(args[0])
        else:
            return self.general_help()
