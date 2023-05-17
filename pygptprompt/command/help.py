# pygptprompt/command/help.py
def display_help(command: str) -> str:
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
    /ls <dir>: List files in directory (defaults to current dir).
    /read <file> [start] [end]: Display file content from start to end line (optional, defaults to full file).
    """
    return help_text.strip()
