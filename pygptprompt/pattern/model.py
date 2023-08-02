"""
pygptprompt/pattern/model.py
"""
from abc import ABC, abstractmethod
from typing import List, Union

from llama_cpp import ChatCompletionMessage, Embedding

from pygptprompt.pattern.mapping import MappingTemplate


class ChatModel(ABC):
    @abstractmethod
    def __init__(self, config: MappingTemplate):
        raise NotImplementedError

    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        # completions will eventually be deprecated
        # according to the OpenAI API documentation.
        raise NotImplementedError

    @abstractmethod
    def get_chat_completion(
        self, messages: List[ChatCompletionMessage]
    ) -> ChatCompletionMessage:
        raise NotImplementedError

    @abstractmethod
    def get_embedding(self, input: Union[str, List[str]]) -> Embedding:
        raise NotImplementedError
