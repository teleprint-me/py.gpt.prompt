import json
import sys
import time
from typing import Any, Optional

import requests
from openai.api import OpenAIAPI, get_api_key
from requests.exceptions import HTTPError


class OpenAIRequests:
    def __init__(self, api_key: Optional[str] = "") -> None:
        self.api = OpenAIAPI(get_api_key(api_key))
        self.session = requests.Session()

    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        url = self.api.url(endpoint)
        headers = self.api.headers
        response = self.session.get(url, headers=headers, params=params)

        # rate limit error
        if response.status_code == 429:
            # retry with exponential back-off
            for i in range(5):
                delay = 2**i
                print(f"Retry {i + 1} in {delay} seconds...")
                time.sleep(delay)
                try:
                    response = self.session.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    break
                except HTTPError as e:
                    print(f"Retry failed: {e}")
        else:
            response.raise_for_status()
        return response.json()

    def post(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        if not params:
            params = {}

        url = self.api.url(endpoint)
        headers = self.api.headers
        response = self.session.post(url, headers=headers, json=params)
        # rate limit error
        if response.status_code == 429:
            # retry with exponential back-off
            for i in range(5):
                delay = 2**i
                print(f"Retry {i + 1} in {delay} seconds...")
                time.sleep(delay)
                try:
                    response = self.session.post(url, headers=headers, json=params)
                    response.raise_for_status()
                    break
                except HTTPError as e:
                    print(f"Retry failed: {e}")
        else:
            response.raise_for_status()
        return response.json()

    def stream(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        # NOTE:
        # This method assumes chat completions endpoint is being used
        # This method may not operate as expected with other endpoints as a result
        if not params:
            params = {}

        url = self.api.url(endpoint)
        headers = self.api.headers
        response = self.session.post(
            url,
            headers=headers,
            json=params,
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
                        if token:  # Skip empty tokens
                            message += token
                            print(token, end="")
                            sys.stdout.flush()
                    except (KeyError,):
                        continue

            # Return the assistant's message after the loop
            return {"role": "assistant", "content": message}
        else:
            print(f"Error: {response.status_code} {response.text}")
            return {}  # Return empty dict in case of an error
