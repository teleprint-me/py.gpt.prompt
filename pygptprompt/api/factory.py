"""
pygptprompt/api/factory.py
"""
from pygptprompt.api.base import BaseAPI
from pygptprompt.api.llama_cpp import LlamaCppAPI
from pygptprompt.api.openai import OpenAIAPI
from pygptprompt.config.manager import ConfigurationManager


class ChatModelFactory:
    """
    A factory for creating chat model instances based on the provider.

    Attributes:
        config (ConfigurationManager): The configuration manager instance.
    """

    def __init__(self, config: ConfigurationManager):
        """
        Initializes the ChatModelFactory with the given configuration manager.

        Args:
            config (ConfigurationManager): The configuration manager instance.
        """
        self.config = config

    def create_model(self, provider) -> BaseAPI:
        """
        Creates and returns a chat model instance based on the provider.

        Args:
            provider (str): The provider key.

        Returns:
            BaseAPI: The chat model instance.

        Raises:
            ValueError: If the provider is unknown.
        """
        provider_config = self.config.get_value(provider)

        if provider_config is None:
            raise ValueError(f"Unknown provider: {provider}")

        provider_key = provider_config["provider"]

        if provider_key == "openai":
            return OpenAIAPI(self.config)
        elif provider_key == "llama_cpp":
            return LlamaCppAPI(self.config)
