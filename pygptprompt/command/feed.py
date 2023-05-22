# pygptprompt/command/feed.py
import feedparser
import requests
from bs4 import BeautifulSoup
from feedparser.util import FeedParserDict


def fetch_rss_feed(feed_url: str) -> FeedParserDict | str:
    try:
        feed: FeedParserDict = feedparser.parse(feed_url)
        return feed
    except Exception as e:
        raise Exception(f"Error fetching RSS feed from {feed_url}: {str(e)}.")


def fetch_article_text(article_url: str) -> str:
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        raise Exception(f"Error fetching article text from {article_url}: {str(e)}.")


def fetch_full_text_from_rss_feed(feed_url: str) -> list[str] | str:
    feed = fetch_rss_feed(feed_url)

    if isinstance(feed, Exception):
        return str(feed)

    full_text_articles = []

    for entry in feed.entries:
        try:
            article_text = fetch_article_text(entry.link)

            # Split the content by newline
            lines = article_text.split("\n")

            # Remove empty lines and append a newline to each line (except the last one)
            cleaned_lines = []
            for index, line in enumerate(lines):
                if line.strip():  # if the line is not empty
                    if index < len(lines) - 1:  # if it's not the last line
                        line += "\n"
                    # If it is the last line, we don't add anything
                    cleaned_lines.append(line)

            # Join the cleaned lines
            cleaned_article_text = "".join(cleaned_lines).strip()

            full_text_articles.append(cleaned_article_text)
        except Exception as e:
            full_text_articles.append(str(e))

    return full_text_articles


def handle_rss_command(command: str) -> str:
    feed_url = command.replace("/rss", "").strip()
    feed_entries = fetch_full_text_from_rss_feed(feed_url)

    if isinstance(feed_entries, list):
        return "\n---\n".join(feed_entries)
    else:
        return feed_entries
