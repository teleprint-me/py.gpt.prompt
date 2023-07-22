"""
pygptprompt/function/factory.py
"""

import json
from typing import Any, Optional

from pygptprompt import logging
from pygptprompt.api.types import ExtendedChatCompletionMessage
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.weather import get_current_weather


class FunctionFactory:
    def __init__(self, config: ConfigurationManager):
        """
        Initialize the FunctionFactory.

        Args:
            config (ConfigurationManager): The configuration manager instance.
        """
        self.functions = {
            "get_current_weather": get_current_weather,
            # Add more functions here as needed
        }

    def get_function_args(
        self, message: ExtendedChatCompletionMessage
    ) -> dict[str, Any]:
        """
        Extract and return the function arguments from the message.

        Args:
            message (ExtendedChatCompletionMessage): The chat completion message.

        Returns:
            dict[str, Any]: A dictionary containing the function arguments. If the function arguments in the message are not valid JSON, prints an error message and returns an empty dictionary.
        """
        function_args = message["function_args"]
        try:
            return json.loads(function_args)
        except json.JSONDecodeError:
            logging.error(f"Invalid function arguments: {function_args}")
            return {}

    def get_function(self, message: ExtendedChatCompletionMessage) -> Optional[object]:
        """
        Get the function specified in the message.

        Args:
            message (ExtendedChatCompletionMessage): The chat completion message.

        Returns:
            Optional[object]: The function specified in the message or None if it doesn't exist.
        """
        function_name = message["function_call"]
        return self.functions.get(function_name)

    def register_function(self, function_name: str, function: object) -> None:
        """
        Register a new function with the FunctionFactory.

        Args:
            function_name (str): The name of the function to register.
            function (object): The function object to register.
        """
        self.functions[function_name] = function
