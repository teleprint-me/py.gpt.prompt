"""
pygptprompt/function/factory.py
"""
import json
import logging
from typing import Any, Callable, List, Optional, Type

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.lazy import LazyFunctionMapper
from pygptprompt.pattern.model import ChatModelResponse


class FunctionFactory:
    def __init__(self, config: ConfigurationManager):
        """
        Initialize the FunctionFactory.

        Args:
            config (ConfigurationManager): The configuration manager instance.
        """
        self.config = config
        self.function_mapper = LazyFunctionMapper()
        self.function_name: str = ""
        self.function_args: dict[str, Any] = {}
        self.function: Optional[Callable] = None
        self.logger = config.get_logger("shadow", self.__class__.__name__)

    def register_function(self, function_name: str, function: Callable) -> None:
        """
        Register a function for lazy loading.

        Args:
            function_name (str): The name to be used for the registered function.
            function (Callable): The function to be registered.
        """
        self.function_mapper.register_function(function_name, function)

    def register_class(self, class_name: str, cls: Type[Any], *args, **kwargs) -> None:
        """
        Register a class for lazy loading.

        Args:
            class_name (str): The name to be used for the registered class.
            cls (Type[Any]): The class to be registered.
            **init_params: Keyword arguments to be passed to the class constructor.
        """
        self.function_mapper.register_class(class_name, cls, *args, **kwargs)

    def map_class_methods(self, class_name: str, methods: List[str]) -> None:
        """
        Map methods of a registered class to functions for lazy loading.

        Args:
            class_name (str): The name of the registered class.
            methods (list[str]): A list of method names to be mapped to functions.
        """
        self.function_mapper.map_class_methods(class_name, methods)

    def get_function_args(self, message: ChatModelResponse) -> dict[str, Any]:
        """
        Extract and return the function arguments from the message.

        Args:
            message (ChatModelResponse): The chat completion message.

        Returns:
            dict[str, Any]: A dictionary containing the function arguments. If the function arguments in the message are not valid JSON, prints an error message and returns an empty dictionary.
        """
        # NOTE: Not all functions require arguments.
        # This is why we always return a dictionary.
        function_call = message.get("function_call", {})
        function_args = function_call.get("arguments")
        if function_args is None:
            self.logger.debug(f"Function arguments is None: {self.function_name}")
            return {}

        try:
            self.function_args = json.loads(function_args)
            return self.function_args
        except json.JSONDecodeError:
            # NOTE: This is an edge case that requires graceful handling.
            self.logger.error(f"Invalid function arguments: {function_args}")
            return {}

    def get_function(self, message: ChatModelResponse) -> Optional[object]:
        """
        Get the function specified in the message.

        Args:
            message (ChatModelResponse): The chat completion message.

        Returns:
            Optional[object]: The function specified in the message or None if it doesn't exist.
        """
        function_call = message.get("function_call")
        self.function_name = function_call.get("name")
        self.function = self.function_mapper.get_function(self.function_name)
        return self.function

    def execute_function(
        self, message: ChatModelResponse
    ) -> Optional[ChatModelResponse]:
        """
        Execute the specified function based on the given message.

        Args:
            message (ChatModelResponse): The chat completion message.

        Returns:
            Optional[ChatModelResponse]: The result of the function execution as a ChatModelResponse, or None if an error occurs.
        """
        # Get the function from the factory
        function = self.get_function(message)
        if function is None:
            self.logger.error(f"Function {message['function_call']} not found.")
            return None

        # Extract the function arguments
        # NOTE: We need to handle the edge case if a JSONDecodeError occurred.
        # We can't block function execution because not all functions require arguments.
        # JSONDecodeError is an edge case that requires graceful handling.
        function_args = self.get_function_args(message)

        try:
            # Log shadow function args
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                # Call the function
                for key, val in function_args.items():
                    self.logger.debug(
                        f"Using function args with key '{key}' and value '{val}'"
                    )
            result = function(**function_args)
        except Exception as e:
            self.logger.error(
                f"Error executing function {message['function_call']}: {e}"
            )
            return None

        # Return a new ChatModelResponse with the result
        return ChatModelResponse(
            role="function", name=self.function_name, content=result
        )
