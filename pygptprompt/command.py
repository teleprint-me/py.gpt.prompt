import os

import feedparser
import requests
from bs4 import BeautifulSoup


def read_file(command: str) -> str:
    filename = command.replace("/read", "").strip()
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"File {filename} not found."


def list_directory(command: str) -> str:
    directory = command.replace("/ls", "").strip()
    try:
        files = os.listdir(directory)
        return "\n".join(files)
    except FileNotFoundError:
        return f"Directory {directory} not found."


def fetch_robots_txt(command: str) -> str:
    url = command.replace("/robots", "").strip()
    # Ensure url starts with http:// or https://
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    try:
        response = requests.get(url + "/robots.txt")
        response.raise_for_status()  # Will raise an exception if the status is 4xx or 5xx
        return response.text
    except Exception as e:
        return f"Could not fetch robots.txt: {str(e)}"


def fetch_rss_feed(feed_url: str):
    feed = feedparser.parse(feed_url)
    return feed


def fetch_article_text(article_url: str):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


def fetch_full_text_from_rss_feed(feed_url: str):
    feed = fetch_rss_feed(feed_url)
    full_text_articles = []
    for entry in feed.entries:
        full_text_articles.append(fetch_article_text(entry.link))
    return full_text_articles


def handle_rss_command(command: str) -> str:
    feed_url = command.replace("/rss", "").strip()
    try:
        feed_entries = fetch_full_text_from_rss_feed(feed_url)
        return "\n---\n".join(feed_entries)  # separate articles with "---"
    except Exception as e:
        return str(e)


def scrape_website(command: str) -> str:
    url = command.replace("/scrape", "").strip()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return str(e)


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
    else:
        content = "Command not recognized."

    return content
