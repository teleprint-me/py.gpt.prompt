# pygptprompt/command/web.py
import os
from typing import Optional
from urllib.parse import urlparse

import html2text
import requests
from requests.exceptions import RequestException

from pygptprompt.session.proxy import SessionQueueProxy

# TODO:
# Always write web content to a file in cache instead of
# automatically injecting it into the message content body.
# This will help avoid unintentional context window overflows.
#
# It would be better to return information about the file instead
# such as token consumption, the number of lines, file name/size,
# etcetera.


# Function to read from cache
def read_from_cache(cache_path: str) -> Optional[str]:
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return f.read()
    return None


# Function to write to cache
def write_to_cache(cache_path: str, content: str) -> None:
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w") as f:
        f.write(content)


# Function to fetch content from the web
def fetch_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        return f"Error fetching content from {url}: {str(e)}."


def convert_html_to_markdown(html: str) -> str:
    h = html2text.HTML2Text()
    # Configure html2text
    h.wrap_links = True
    h.single_line_break = True
    h.mark_code = True
    h.wrap_list_items = True
    h.wrap_tables = True
    h.re_md_chars_matcher_all = True
    return h.handle(html).strip()


class RobotsFetcher:
    def __init__(self, queue_proxy: SessionQueueProxy):
        self.queue_proxy = queue_proxy

    # Function to fetch and cache robots.txt
    def execute(self, command: str) -> str:
        # Command is split into parts
        args = command.split()
        # URL is the second part (index 1)
        url = args[1].strip()
        # Get the storage path
        storage_path = self.queue_proxy.config.get_value("path.storage", "storage")

        # Ensure URL starts with "http://" or "https://", and ends with "/robots.txt"
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        if not url.endswith("/robots.txt"):
            url += "/robots.txt"

        # Create a path for the cache
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        cache_path = os.path.join(storage_path, "robots", domain, "robots.txt")

        # Try to read from cache
        cached_content = read_from_cache(cache_path)
        if cached_content is not None:
            return cached_content

        # If the cache does not exist, fetch the robots.txt
        content = fetch_content(url)

        # Cache the response
        write_to_cache(cache_path, content)

        return content


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
            return markdown_content

        # If the cache does not exist, fetch the HTML content
        html_content = self._fetch_html_content(html_path, url)

        # Convert HTML to markdown
        markdown_content = convert_html_to_markdown(html_content)
        markdown_content_size = self.queue_proxy.token.get_content_count(
            markdown_content
        )

        # Cache the markdown content
        write_to_cache(markdown_path, markdown_content)

        # Check if the content is too large
        if markdown_content_size > self.queue_proxy.token.base_limit:
            # Return a message indicating that the output was too large and has been saved to a file
            return f"The content is too large to display. It has been saved to a file: {markdown_path}"

        return markdown_content

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
