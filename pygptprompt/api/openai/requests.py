# pygptprompt/openai/requests.py
import json
import sys
import time
from typing import Any, Optional

import requests
from requests.exceptions import HTTPError

from pygptprompt.openai.api import OpenAIAPI


class OpenAIRequests:
    MAX_RETRIES = 5

    def __init__(self, api_key: Optional[str] = "") -> None:
        self.api = OpenAIAPI(api_key or "")
        self.session = requests.Session()

    def _handle_rate_limit(
        self,
        method: str,
        url: str,
        headers: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> requests.Response:
        for i in range(self.MAX_RETRIES):
            delay = 2**i
            print(f"OpenAIAPIError: Retry {i + 1} in {delay} seconds...")
            time.sleep(delay)
            try:
                response = self.session.request(
                    method, url, headers=headers, json=params, stream=stream
                )
                response.raise_for_status()
                return response
            except HTTPError as e:
                print(f"OpenAIAPIError: Retry failed: {e}")
        raise HTTPError("Max retries exceeded")

    def _send_request(
        self,
        method: str,
        url: str,
        headers: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> requests.Response:
        response = self.session.request(
            method, url, headers=headers, json=params, stream=stream
        )
        if response.status_code == 429:
            response = self._handle_rate_limit(method, url, headers, params, stream)
        response.raise_for_status()
        return response

    def _process_stream_response(self, response: requests.Response) -> dict[str, Any]:
        message = ""
        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    line = line[6:]
                if line == "[DONE]":
                    break
                json_line = json.loads(line)
                try:
                    token = json_line["choices"][0]["delta"]["content"]
                    if token:
                        message += token
                        print(token, end="")
                        sys.stdout.flush()
                except KeyError:
                    continue
        print()
        sys.stdout.flush()
        return {"role": "assistant", "content": message}

    def get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> dict[str, Any]:
        url = self.api.url(endpoint)
        headers = self.api.headers
        response = self._send_request("GET", url, headers, params, stream)
        if stream:
            return self._process_stream_response(response)
        else:
            return response.json()

    def post(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        stream: bool = False,
    ) -> dict[str, Any]:
        url = self.api.url(endpoint)
        headers = self.api.headers
        response = self._send_request("POST", url, headers, params, stream)
        if stream:
            return self._process_stream_response(response)
        else:
            return response.json()

    def stream(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        url = self.api.url(endpoint)
        headers = self.api.headers
        response = self._send_request("POST", url, headers, params, True)
        return self._process_stream_response(response)
