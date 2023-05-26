from typing import Any, Optional

from pygptprompt.openai.requests import OpenAIRequests


class OpenAICompletions(OpenAIRequests):
    def completions(
        self,
        prompt: str | list[str],
        model: Optional[str] = "text-davinci-003",
        max_tokens: Optional[int] = 256,
        temperature: Optional[float] = 0.5,
        **params,
    ) -> dict[str, Any]:
        keys = ["prompt", "model", "max_tokens", "temperature"]
        values = [prompt, model, max_tokens, temperature]
        for key, value in zip(keys, values):
            params[key] = value
        return self.post("/completions", params=params)

    def chat_completions(
        self,
        messages: list[dict[str, str]],
        model: Optional[str] = "gpt-3.5-turbo",
        max_tokens: Optional[int] = 512,
        temperature: Optional[float] = 0.5,
        **params,
    ) -> dict[str, Any]:
        keys = ["messages", "model", "max_tokens", "temperature"]
        values = [messages, model, max_tokens, temperature]
        for key, value in zip(keys, values):
            params[key] = value
        return self.post("/chat/completions", params=params)

    def stream_chat_completions(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 512,
        temperature: float = 0.5,
        **params,
    ) -> dict[str, Any]:
        # `{"stream": True}` enables REST API streaming
        keys = ["messages", "model", "max_tokens", "temperature", "stream"]
        values = [messages, model, max_tokens, temperature, True]
        for key, value in zip(keys, values):
            params[key] = value
        return self.stream("/chat/completions", params=params)
