import json
import os
import subprocess

import feedparser
import requests
from bs4 import BeautifulSoup
from feedparser.util import FeedParserDict

# Load the configuration
with open("config.json", "r") as f:
    config = json.load(f)


def read_file(command: str) -> str:
    args = command.replace("/read", "").strip().split(" ")

    # First argument is the filename
    filename = args[0]
    if not os.path.isfile(filename):
        return f"Error: File {filename} not found."

    abs_path = os.path.abspath(filename)

    # Get allowed and denied paths from the configuration
    allowed_paths = config["allowed_paths"]
    denied_paths = config["denied_paths"]

    if any(abs_path.startswith(path) for path in denied_paths):
        return "RoleError: Accessed denied! You shouldn't snoop in private places."

    if not any(abs_path.startswith(path) for path in allowed_paths):
        return "RoleError: Accessed denied! You shouldn't snoop in private places."

    # Optional starting line number
    start_line = (
        0 if len(args) < 2 else int(args[1]) - 1
    )  # -1 to account for 0-indexing

    # Optional ending line number
    end_line = None if len(args) < 3 else int(args[2])

    if end_line is not None and end_line <= start_line:
        return "Error: Ending line number must be greater than starting line number."

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            if end_line is None:
                return "".join(lines[start_line:])
            else:
                return "".join(lines[start_line:end_line])
    except Exception as e:
        return f"Error reading file {filename}: {str(e)}."


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


def fetch_robots_txt(command: str) -> str:
    url = command.replace("/robots", "").strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        response = requests.get(url + "/robots.txt")
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching robots.txt from {url}: {str(e)}."


def fetch_rss_feed(feed_url: str) -> FeedParserDict | str:
    try:
        feed: FeedParserDict = feedparser.parse(feed_url)
        return feed
    except Exception as e:
        raise Exception(f"Error fetching RSS feed from {feed_url}: {str(e)}.")


def fetch_article_text(article_url: str):
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        raise Exception(f"Error fetching article text from {article_url}: {str(e)}.")


def fetch_full_text_from_rss_feed(feed_url: str):
    feed = fetch_rss_feed(feed_url)
    if isinstance(feed, Exception):
        return str(feed)

    full_text_articles = []
    for entry in feed.entries:
        try:
            full_text_articles.append(fetch_article_text(entry.link))
        except Exception as e:
            full_text_articles.append(str(e))
    return full_text_articles


def handle_rss_command(command: str) -> str:
    feed_url = command.replace("/rss", "").strip()
    feed_entries = fetch_full_text_from_rss_feed(feed_url)
    return "\n---\n".join(feed_entries)


def scrape_website(command: str) -> str:
    url = command.replace("/scrape", "").strip()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Error scraping website {url}: {str(e)}."


def display_help(command: str) -> str:
    help_text = """
    Here are the available commands:

    /read <filename> [start_line] [end_line] - Read contents of a file.
        - If start_line is provided, then reading will begin from that line.
        - If end_line is provided, then reading will stop at that line.
        - Line numbers start at 1.
    /ls <directory>: Lists files in the given directory.
    /scrape <url>: Scrapes the text from the given URL.
    /robots <url>: Fetches the robots.txt file from the given URL.
    /rss <feed_url>: Fetches and displays full text articles from the given RSS feed.
    """
    return help_text.strip()


def handle_command(command: str) -> str:
    if command.startswith("/read"):
        content = read_file(command)
    elif command.startswith("/ls"):
        content = list_directory(command)
    elif command.startswith("/scrape"):
        content = scrape_website(command)
    elif command.startswith("/robots"):
        content = fetch_robots_txt(command)
    elif command.startswith("/rss"):
        content = handle_rss_command(command)
    elif command.startswith("/help"):
        content = display_help(command)
    else:
        content = "Command not recognized."

    return content
