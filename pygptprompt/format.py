import re

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML


def print_bold(text: str) -> None:
    print_formatted_text(HTML(f"<b>{text}</b>"))


def print_with_backticks_bold(text):
    bold_text = re.sub(r"`(.*?)`", r"<b>\1</b>", text)
    print_formatted_text(HTML(bold_text))


if __name__ == "__main__":
    # Usage:
    print_with_backticks_bold("Hello, `world`!")
