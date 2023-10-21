"""
pygptprompt/function/lazy.py

This module defines classes and functions related to lazy loading of functions and classes.

# Usage Prerequisites
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.lazy import LazyFunctionMapper
from pygptprompt.function.memory import SQLiteMemoryFunction

config = ConfigurationManager("tests/config.dev.json")

# `LazyFunctionMapper` Usage
function_mapper = LazyFunctionMapper()

function_mapper.register_class(
    "SQLiteMemoryFunction",
    SQLiteMemoryFunction,
    table_name="test",
    config=config,
)

function_mapper.map_class_methods("SQLiteMemoryFunction", ["query_memory", "update_memory", "get_all_keys"])

update_memory = function_mapper.functions["SQLiteMemoryFunction_update_memory"]
print(update_memory("test", "this is just a test"))
print()

query_memory = function_mapper.functions["SQLiteMemoryFunction_query_memory"]
print(query_memory("test"))
print()

get_all_keys = function_mapper.functions["SQLiteMemoryFunction_get_all_keys"]
print(get_all_keys())
print()
"""
from typing import Any, Callable, Dict, Type


class LazyFunctionWrapper:
    """
    Wrapper class for lazily initializing a class instance.

    This class is used to defer the initialization of an instance of a class until it is actually needed.

    Args:
        cls (Type[Any]): The class to be instantiated.
        *args: Positional arguments to be passed to the class constructor.
        **kwargs: Keyword arguments to be passed to the class constructor.

    Attributes:
        cls (Type[Any]): The class to be instantiated.
        args: Positional arguments to be passed to the class constructor.
        kwargs: Keyword arguments to be passed to the class constructor.
        instance: The instance of the class once it is initialized.
    """

    def __init__(self, cls, *args, **kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs
        self.instance = None

    def __call__(self, *args, **kwargs):
        """
        Call method to lazily initialize and return the class instance.

        Args:
            *args: Positional arguments to be passed to the class constructor.
            **kwargs: Keyword arguments to be passed to the class constructor.

        Returns:
            Any: The instance of the class.
        """
        if self.instance is None:
            self.instance = self.cls(*self.args, **self.kwargs)
        return self.instance


class LazyFunctionMapper:
    """
    Mapper class for managing lazy loading of functions and classes.

    This class allows you to register functions and classes for lazy loading and provides methods
    for instantiating classes and mapping class methods to functions.

    Attributes:
        _functions (Dict[str, Callable]): A dictionary mapping function names to their corresponding functions.
        _classes (Dict[str, Type[Any]]): A dictionary mapping class names to their corresponding classes.
        _class_configurations (Dict[str, LazyFunctionWrapper]): A dictionary mapping class names to LazyFunctionWrapper instances.
    """

    def __init__(self):
        self._functions = {}
        self._classes = {}
        self._class_configurations = {}

    @property
    def functions(self) -> Dict[str, Callable]:
        """
        Property to access the registered functions.

        Returns:
            Dict[str, Callable]: A dictionary mapping function names to their corresponding functions.
        """
        return self._functions

    def get_function(self, name: str) -> Callable:
        return self._functions.get(name)

    def register_function(self, function_name: str, function: Callable) -> None:
        """
        Register a function for lazy loading.

        Args:
            function_name (str): The name to be used for the registered function.
            function (Callable): The function to be registered.
        """
        self._functions[function_name] = function

    def register_class(self, class_name: str, cls: Type[Any], *args, **kwargs) -> None:
        """
        Register a class for lazy loading.

        Args:
            class_name (str): The name to be used for the registered class.
            cls (Type[Any]): The class to be registered.
            *args: Arguments to be passed to the class constructor.
            **kwargs: Keyword arguments to be passed to the class constructor.
        """
        self._classes[class_name] = cls
        self._class_configurations[class_name] = LazyFunctionWrapper(
            cls, *args, **kwargs
        )

    def instantiate_class(self, class_name: str):
        """
        Instantiate a class registered for lazy loading.

        Args:
            class_name (str): The name of the registered class to be instantiated.

        Returns:
            Any: The instance of the class.

        Raises:
            ValueError: If the specified class name is not registered.
        """
        if class_name in self._class_configurations:
            return self._class_configurations[class_name]()
        else:
            raise ValueError(f"No registered class with the name {class_name}")

    def map_class_methods(self, class_name: str, methods: list[str]) -> None:
        """
        Map methods of a registered class to functions for lazy loading.

        Args:
            class_name (str): The name of the registered class.
            methods (list[str]): A list of method names to be mapped to functions.
        """
        instance = self.instantiate_class(class_name)
        for method_name in methods:
            method = getattr(instance, method_name)
            if callable(method):
                self._functions[f"{class_name}_{method_name}"] = method
