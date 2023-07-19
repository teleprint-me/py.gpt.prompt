# pygptprompt/session/model.py
from pygptprompt import SYSTEM_MESSAGE
from pygptprompt.setting.config import GlobalConfiguration


class SessionModel:
    def __init__(self, config: GlobalConfiguration):
        self.config: GlobalConfiguration = config

    @property
    def name(self) -> str:
        return self.config.get_value("chat_completions.model", "gpt-3.5-turbo")

    @property
    def max_tokens(self) -> int:
        return self.config.get_value("chat_completions.max_tokens", 1024)

    @property
    def temperature(self) -> float:
        return self.config.get_value("chat_completions.temperature", 0.5)

    @property
    def system_message(self) -> dict[str, str]:
        return self.config.get_value("chat_completions.system_message", SYSTEM_MESSAGE)
