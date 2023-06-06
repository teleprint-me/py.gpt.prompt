# tests/unit/test_openai.py
from typing import Any

import pytest

from pygptprompt.openai import OpenAI


class TestOpenAI:
    @pytest.mark.private
    def test_streaming_completions(
        self,
        openai: OpenAI,
        chat_completion: list[dict[str, str]],
    ):
        model = "gpt-3.5-turbo"
        temperature = 0
        max_tokens = 128

        message: dict[str, Any] = openai.completions.stream_chat_completions(
            chat_completion, model, max_tokens, temperature
        )

        print()

        assert (
            message["content"]
            == '"Le renard brun rapide a sauté par-dessus le chien paresseux."'
        )
