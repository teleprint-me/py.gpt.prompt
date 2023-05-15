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
