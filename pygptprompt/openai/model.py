from typing import Any

from .requests import OpenAIRequests


class OpenAIModel(OpenAIRequests):
    def list(self) -> dict[str, Any]:
        return self.get("/models")

    def retrieve(self, model: str) -> dict[str, Any]:
        return self.get(f"/models/{model}")
