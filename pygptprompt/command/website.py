# pygptprompt/command/website.py
import os
from urllib.parse import urlparse

from pygptprompt.command.webtools import (
    convert_html_to_markdown,
    fetch_content,
    read_from_cache,
    write_to_cache,
)
from pygptprompt.session.proxy import SessionQueueProxy


class WebsiteFetcher:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    def execute(self, command: str) -> str:
        # Parse the command and get the URL
        url = self._parse_command(command)

        # Get the paths for the cache
        html_path, markdown_path = self._get_cache_paths(url)

        # Try to read from cache
        markdown_content = read_from_cache(markdown_path)
        if markdown_content is not None:
            return self.queue_proxy.handle_content_size(markdown_content, markdown_path)

        # If the cache does not exist, fetch the HTML content
        html_content = self._fetch_html_content(html_path, url)

        # Convert HTML to markdown
        markdown_content = convert_html_to_markdown(html_content)

        # Cache the markdown content
        write_to_cache(markdown_path, markdown_content)

        return self.queue_proxy.handle_content_size(markdown_content, markdown_path)

    def _parse_command(self, command: str) -> str:
        # Command is first argument
        args = command.split()
        # URL is second argument
        url = args[1].strip()

        # Ensure URL starts with "http://" or "https://"
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    def _get_cache_paths(self, url: str) -> tuple[str, str]:
        # Get the storage path
        storage_path = self.queue_proxy.config.get_value("path.storage", "storage")

        # Create paths for the cache
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Remove leading slash
        # If path is empty, use 'index' as the default filename
        path = parsed_url.path.lstrip("/") or "index.html"
        html_path = os.path.join(storage_path, "html", domain, path)

        markdown_path = os.path.join(
            storage_path,
            "markdown",
            domain,
            f"{os.path.splitext(path)[0]}.md",
        )

        return html_path, markdown_path

    def _fetch_html_content(self, html_path: str, url: str) -> str:
        html_content = read_from_cache(html_path)
        if html_content is None:
            html_content = fetch_content(url)

            # Cache the HTML content
            write_to_cache(html_path, html_content)

        return html_content
