import os
from typing import Optional
from urllib.parse import urlparse

import html2text
import requests
from requests.exceptions import RequestException

from pygptprompt.config import get_config

# Load the configuration
__config__ = get_config()

STORAGE_DIR = __config__.get(
    "storage_dir", "storage"
)  # default to 'storage' if not set


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


# Function to fetch and cache robots.txt
def fetch_robots_txt(command: str) -> str:
    # Command is split into parts
    args = command.split()
    # URL is the second part (index 1)
    url = args[1].strip()

    # Ensure URL starts with "http://" or "https://", and ends with "/robots.txt"
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    if not url.endswith("/robots.txt"):
        url += "/robots.txt"

    # Create a path for the cache
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    cache_path = os.path.join(STORAGE_DIR, "robots", domain, "robots.txt")

    # Try to read from cache
    cached_content = read_from_cache(cache_path)
    if cached_content is not None:
        return f"```txt\n{cached_content}```"

    # If the cache does not exist, fetch the robots.txt
    content = fetch_content(url)

    # Cache the response
    write_to_cache(cache_path, content)

    return f"```txt\n{content}```"


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


def fetch_and_store_website(command: str) -> str:
    # Command is first argument
    args = command.split()
    # URL is second argument
    url = args[1].strip()

    # Ensure URL starts with "http://" or "https://"
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Create paths for the cache
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.lstrip("/")  # remove leading slash
    html_path = os.path.join(STORAGE_DIR, "html", domain, path)
    markdown_path = os.path.join(
        STORAGE_DIR, "markdown", domain, f"{os.path.splitext(path)[0]}.md"
    )

    # Try to read from cache
    markdown_content = read_from_cache(markdown_path)
    if markdown_content is not None:
        return f"```md\n{markdown_content}\n```"

    # If the cache does not exist, fetch the HTML content
    html_content = read_from_cache(html_path)
    if html_content is None:
        html_content = fetch_content(url)

        # Cache the HTML content
        write_to_cache(html_path, html_content)

    # Convert HTML to markdown
    markdown_content = convert_html_to_markdown(html_content)

    # Cache the markdown content
    write_to_cache(markdown_path, markdown_content)

    return f"```md\n{markdown_content}\n```"
