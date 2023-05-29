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

    # Add other methods and properties as needed
