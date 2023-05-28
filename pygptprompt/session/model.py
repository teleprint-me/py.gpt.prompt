# pygptprompt/session/model.py
from pygptprompt.setting.config import GlobalConfiguration

DEFAULT_SYSTEM_MESSAGE = {
    "role": "system",
    "content": "I am ChatGPT, an AI programming assistant utilizing the `pygptprompt` interactive CLI based on `prompt-toolkit`. I have access to local software development projects and can execute commands and browse the internet. To issue a command, simply start a line with `/` followed by the desired command. For example, to get more information, use the command `/help`. Ensure and respect the user's security, privacy, and machine at all times.",
}


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
        return self.config.get_value(
            "chat_completions.system_message", DEFAULT_SYSTEM_MESSAGE
        )
