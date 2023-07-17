from abc import ABC, abstractmethod


class BaseAPI(ABC):
    @abstractmethod
    def get_completions(self, **kwargs):
        # completions will eventually be deprecated
        # according to the OpenAI API documentation.
        raise NotImplementedError

    @abstractmethod
    def get_chat_completions(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_embeddings(self, **kwargs):
        raise NotImplementedError
