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
        provider_map (dict): A dictionary mapping provider keys to their corresponding classes.
    """

    def __init__(self, config: ConfigurationManager):
        """
        Initializes the ChatModelFactory with the given configuration manager.

        Args:
            config (ConfigurationManager): The configuration manager instance.
        """
        self.config = config
        self.provider_map = {
            "openai": OpenAIAPI,
            "llama_cpp": LlamaCppAPI,
        }

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

        if provider_config is None or "provider" not in provider_config:
            raise ValueError(f"Unknown provider: {provider}")

        provider_key = provider_config["provider"]

        if provider_key not in self.provider_map:
            raise ValueError(f"Unknown provider: {provider}")

        return self.provider_map[provider_key](self.config)
