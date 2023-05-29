# pygptprompt/command/robots.py
import os
from urllib.parse import urlparse

from pygptprompt.command.webtools import fetch_content, read_from_cache, write_to_cache
from pygptprompt.session.proxy import SessionQueueProxy


class RobotsFetcher:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    def execute(self, command: str) -> str:
        # Parse the command and get the URL
        url = self._parse_command(command)

        # Get the paths for the cache
        cache_path = self._get_cache_path(url)

        # Try to read from cache
        cached_content = read_from_cache(cache_path)
        if cached_content is not None:
            return self.queue_proxy.handle_content_size(cached_content, cache_path)

        # If the cache does not exist, fetch the robots.txt content
        content = self._fetch_content(cache_path, url)

        return self.queue_proxy.handle_content_size(content, cache_path)

    def _parse_command(self, command: str) -> str:
        # Command is split into parts
        args = command.split()
        # URL is the second part (index 1)
        url = args[1].strip()

        # Ensure URL starts with "http://" or "https://", and ends with "/robots.txt"
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if not url.endswith("/robots.txt"):
            url += "/robots.txt"

        return url

    def _get_cache_path(self, url: str) -> str:
        # Get the storage path
        storage_path = self.queue_proxy.config.get_value("path.storage", "storage")

        # Create a path for the cache
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        cache_path = os.path.join(storage_path, "robots", domain, "robots.txt")

        return cache_path

    def _fetch_content(self, cache_path: str, url: str) -> str:
        # Fetch the robots.txt
        content = fetch_content(url)

        # Cache the response
        write_to_cache(cache_path, content)

        return content
