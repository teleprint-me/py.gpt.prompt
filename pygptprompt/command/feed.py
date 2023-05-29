# pygptprompt/command/feed.py
import os
from typing import Union
from urllib.parse import urlparse

import feedparser
import requests
from bs4 import BeautifulSoup
from feedparser.util import FeedParserDict

from pygptprompt.command.webtools import read_from_cache, write_to_cache
from pygptprompt.session.proxy import SessionQueueProxy


class RSSHandler:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    def execute(self, command: str) -> str:
        # Parse the command and get the feed URL
        feed_url = self._parse_command(command)

        # Cache the content
        cache_path = self._get_cache_path(feed_url)

        # Try to read from cache
        cached_content = read_from_cache(cache_path)
        if cached_content is not None:
            return self.queue_proxy.handle_content_size(cached_content, cache_path)

        # Fetch the full text from the RSS feed
        feed_entries = self._fetch_full_text_from_rss_feed(feed_url)

        # If the feed_entries is a list, join them with "\n---\n"
        if isinstance(feed_entries, list):
            feed_entries_content = "\n---\n".join(feed_entries)
        else:  # something went wrong...
            return feed_entries  # return the error instead.

        # Always cache the result!
        write_to_cache(cache_path, feed_entries_content)

        return self.queue_proxy.handle_content_size(feed_entries_content, cache_path)

    def _parse_command(self, command: str) -> str:
        # Command is split into parts
        args = command.strip().split()
        # URL is the second part (index 1)
        url = args[1]

        # Ensure URL starts with "http://" or "https://"
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    def _get_cache_path(self, feed_url: str) -> str:
        # Get the storage path
        storage_path = self.queue_proxy.config.get_value("path.storage", "storage")

        # Create a path for the cache
        parsed_url = urlparse(feed_url)
        domain = parsed_url.netloc
        cache_path = os.path.join(storage_path, "rss", domain, "feed.txt")

        return cache_path

    def _fetch_rss_feed(self, feed_url: str) -> Union[str, FeedParserDict]:
        try:
            feed: FeedParserDict = feedparser.parse(feed_url)
            # Check if the feed is empty
            if not feed.entries:
                return f"Error: The URL {feed_url} does not appear to be an RSS feed."
            return feed
        except Exception as e:
            return f"Error fetching RSS feed from {feed_url}: {str(e)}."

    def _fetch_article_text(self, article_url: str) -> str:
        try:
            response = requests.get(article_url)
            print(f"Response status code: {response.status_code}")  # Debugging line
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            print(f"Extracted text: {text[:100].strip()}...")  # Debugging line
            return text
        except Exception as e:
            return f"Error fetching article text from {article_url}: {str(e)}."

    def _fetch_cleaned(self, article_text: str) -> str:
        # Split the content by newline
        lines: list[str] = article_text.split("\n")
        # Remove empty lines and append a newline to each line (except the last one)
        cleaned_lines = []
        for index, line in enumerate(lines):
            if line.strip():  # if the line is not empty
                if index < len(lines) - 1:  # if it's not the last line
                    line += "\n"
                # If it is the last line, we don't add anything
                cleaned_lines.append(line)
        # Join the cleaned lines
        return "".join(cleaned_lines).strip()

    def _fetch_full_text_from_rss_feed(self, feed_url: str) -> Union[str, list[str]]:
        feed = self._fetch_rss_feed(feed_url)

        if isinstance(feed, str):
            return feed

        full_text_articles = []

        for entry in feed.entries:
            article_text = self._fetch_article_text(entry.link)
            if isinstance(article_text, str):
                cleaned_article_text = self._fetch_cleaned(article_text)
                full_text_articles.append(cleaned_article_text)
            else:
                full_text_articles.append(article_text)

        return full_text_articles
