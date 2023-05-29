# pygptprompt/session/proxy.py
from pygptprompt.session.queue import SessionQueue


class SessionQueueProxy:
    def __init__(self, session_queue: SessionQueue):
        self._session_queue: SessionQueue = session_queue

    @property
    def config(self):
        return self._session_queue.config

    @property
    def policy(self):
        return self._session_queue.policy

    @property
    def token(self):
        return self._session_queue.token

    def handle_content_size(self, content: str, cache_path: str) -> str:
        content_size = self.token.get_content_count(content)
        if content_size > self.token.base_limit:
            return f"The content is too large to display. It has been saved to a file: {cache_path}"
        return content
