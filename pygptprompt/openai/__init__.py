from typing import Optional

from .api import get_api_key
from .completions import OpenAICompletions
from .model import OpenAIModel
from .requests import OpenAIRequests


class OpenAI:
    def __init__(self, api_key: Optional[str] = "") -> None:
        api_key = get_api_key(api_key)

        self.requests = OpenAIRequests(api_key)
        self.completions = OpenAICompletions(api_key)
        self.model = OpenAIModel(api_key)
