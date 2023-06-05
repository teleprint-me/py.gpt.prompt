from typing import Optional

from .completions import OpenAICompletions
from .model import OpenAIModel
from .requests import OpenAIRequests


class OpenAI:
    def __init__(self, api_key: Optional[str] = "") -> None:
        self.requests = OpenAIRequests(api_key)
        self.completions = OpenAICompletions(api_key)
        self.model = OpenAIModel(api_key)
