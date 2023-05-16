def display_help(command: str) -> str:
    help_text = """
    # Help

    ## Commands:

    ### Web Pages
    /robots <url>: Get robots.txt of URL.
    /browse <url>: Fetch HTML from URL, convert to Markdown, and cache it locally. Returns local cache if content already exists.

    ### RSS Feeds
    /rss <url>: Fetch and display full text articles from RSS feed.

    ### Filesystem (access restricted by configuration)
    /ls <dir>: List files in local directory.
    /read <file> [start_line] [end_line]: Read local file content from start_line to end_line (end_line is optional and line numbers start at 1).
    /tree <directory> [--ignore dir1,dir2,...]: Display directory and file structure in a tree format. Optionally, ignore specified directories.
    """
    return help_text.strip()
