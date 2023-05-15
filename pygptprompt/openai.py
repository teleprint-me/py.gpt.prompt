import json
import sys

import requests


class OpenAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.chat_completions_url = "https://api.openai.com/v1/chat/completions"

    def chat_completions(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> dict[str, str] | None:
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        response = requests.post(
            self.chat_completions_url,
            headers=self.headers,
            json=data,
        )

        if response.status_code == 200:
            payload = response.json()
            message = payload["choices"][0]["message"]
            print(message["content"])
            return message
        else:
            print(f"Error: {response.status_code} {response.text}")
            return None  # Return None in case of an error

    def stream_chat_completions(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 512,
        temperature: float = 0.7,
    ) -> dict[str, str] | None:
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,  # Enable REST API streaming
            "messages": messages,
        }

        response = requests.post(
            self.chat_completions_url,
            headers=self.headers,
            json=data,
            stream=True,  # Enable HTTP token streaming
        )

        if response.status_code == 200:
            message = ""
            # Iterate over the response data one line at a time
            for line in response.iter_lines():
                # If the line is not empty
                if line:
                    # Decode it to string
                    line = line.decode("utf-8")

                    # Check if the line starts with 'data: '
                    if line.startswith("data: "):
                        # If it does, strip it out
                        line = line[6:]

                    # If the line is '[DONE]', stop processing
                    if line == "[DONE]":
                        break

                    json_line = json.loads(line)

                    try:
                        # Aggregate and flush the tokens to output
                        token = json_line["choices"][0]["delta"]["content"]
                        if token:
                            message += token
                            print(token, end="")
                            sys.stdout.flush()
                    except (KeyError,):
                        continue

            # Return the assistant's message after the loop
            return {"role": "assistant", "content": message}
        else:
            print(f"Error: {response.status_code} {response.text}")
            return None  # Return None in case of an error
