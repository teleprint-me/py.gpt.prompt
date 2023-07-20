from abc import ABC, abstractmethod
from typing import List, Union

from llama_cpp import ChatCompletionMessage

from pygptprompt.config.manager import ConfigurationManager


class BaseAPI(ABC):
    @abstractmethod
    def __init__(self, config: ConfigurationManager):
        raise NotImplementedError

    @abstractmethod
    def get_completions(self, prompt: str):
        # completions will eventually be deprecated
        # according to the OpenAI API documentation.
        raise NotImplementedError

    @abstractmethod
    def get_chat_completions(self, messages: List[ChatCompletionMessage]):
        raise NotImplementedError

    @abstractmethod
    def get_embeddings(self, input: Union[str, List[str]]):
        raise NotImplementedError
