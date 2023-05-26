import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def get_api_key(api_key: Optional[str] = "") -> str:
    return api_key or os.getenv("OPENAI_API_KEY") or ""


@dataclass
class OpenAIAPI:
    """A class to manage OpenAI API information"""

    _api_key: str = os.getenv("OPENAI_API_KEY") or ""
    _org_id: str = os.getenv("OPENAI_ORGANIZATION_ID") or ""

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def org_id(self) -> str:
        return self._org_id

    @property
    def base_url(self) -> str:
        return "https://api.openai.com"

    @property
    def headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers.update({"Authorization": f"Bearer {self.api_key}"})
        if self.org_id:
            headers.update({"OpenAI-Organization": self.org_id})
        return headers

    @property
    def version(self) -> int:
        return 1

    def path(self, endpoint: str) -> str:
        if endpoint.startswith(f"/v{self.version}"):
            return endpoint
        return f'/v{self.version}/{endpoint.lstrip("/")}'

    def url(self, endpoint: str) -> str:
        return f'{self.base_url}/{self.path(endpoint).lstrip("/")}'
