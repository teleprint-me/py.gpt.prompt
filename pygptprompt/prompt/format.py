# pygptprompt/prompt/format.py
import re
from typing import Any

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from pygptprompt.setting.config import GlobalConfiguration

DEFAULT_STYLE: dict[str, Any] = {"italic": "italic", "bold": "bold"}


class FormatText:
    def __init__(self, config: GlobalConfiguration):
        styles = config.get_value("style", DEFAULT_STYLE)
        self.style = Style.from_dict(styles)

    def print_bold(self, text: str) -> None:
        print_formatted_text(HTML(f"<b>{text}</b>"), style=self.style)

    def print_with_backticks_bold(self, text: str) -> None:
        bold_text = re.sub(r"`(.*?)`", r"<b>\1</b>", text)
        print_formatted_text(HTML(bold_text), style=self.style)

    def print_italic(self, text: str) -> None:
        print_formatted_text(HTML(f"<italic>{text}</italic>"), style=self.style)


if __name__ == "__main__":
    # Usage:
    from pygptprompt.setting.config import GlobalConfiguration

    config = GlobalConfiguration()
    formatter = FormatText(config)
    formatter.print_with_backticks_bold("Hello, `world`!")
