# pygptprompt/command/webtools.py
import os
from typing import Optional

import html2text
import requests
from requests.exceptions import RequestException


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
        return f"RequestError: Error fetching content from {url}: {str(e)}."


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
