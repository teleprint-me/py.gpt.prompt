import os
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


def fetch_robots_txt(command: str) -> str:
    url = command.replace("/robots", "").strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        response = requests.get(url + "/robots.txt")
        response.raise_for_status()
        return response.text
    except RequestException as e:
        return f"Error fetching robots.txt from {url}: {str(e)}."


def fetch_html_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        return f"Error fetching HTML content from {url}: {str(e)}."


def store_content(directory: str, filename: str, content: str):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, filename), "w") as file:
        file.write(content)


def convert_html_to_markdown(html: str) -> str:
    h = html2text.HTML2Text()
    h.wrap_links = True
    h.single_line_break = True
    h.mark_code = True
    h.wrap_list_items = True
    h.wrap_tables = True
    h.re_md_chars_matcher_all = True
    return h.handle(html).strip()


def fetch_and_store_website(command: str) -> str:
    url = command.replace("/browse", "").strip()

    # Check if the URL is valid
    if not url.startswith(("http://", "https://")):
        return "Error: Invalid URL."

    # Check if the content already exists locally
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.lstrip("/")  # remove leading slash

    # Deduce file names
    html_filename = f"{os.path.splitext(os.path.basename(path))[0]}.html"
    md_filename = f"{os.path.splitext(os.path.basename(path))[0]}.md"

    # Deduce directory paths without filename
    html_dir = os.path.join(STORAGE_DIR, "html", domain, os.path.dirname(path))
    markdown_dir = os.path.join(STORAGE_DIR, "markdown", domain, os.path.dirname(path))

    html_exists = os.path.exists(os.path.join(html_dir, html_filename))
    md_exists = os.path.exists(os.path.join(markdown_dir, md_filename))

    if html_exists and md_exists:
        # Return the locally stored content
        with open(os.path.join(markdown_dir, md_filename), "r") as f:
            markdown_content = f.read()
        return f"```md\n{markdown_content}\n```"

    try:
        # Check if the HTML content already exists locally
        if html_exists:
            # Read the HTML content from the local file
            with open(os.path.join(html_dir, html_filename), "r") as f:
                html_content = f.read()
        else:
            # Fetch the HTML content
            html_content = fetch_html_content(url)

            # Store the HTML content
            store_content(html_dir, html_filename, html_content)

        # Convert HTML to markdown
        markdown_content = convert_html_to_markdown(html_content)

        # Store the markdown content
        store_content(markdown_dir, md_filename, markdown_content)

        return f"```md\n{markdown_content}\n```"

    except Exception as e:
        return f"Error fetching request for {url}: {str(e)}."
