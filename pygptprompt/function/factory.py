"""
pygptprompt/function/factory.py
"""

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.weather import get_current_weather


class FunctionFactory:
    def __init__(self, config: ConfigurationManager):
        self.functions = {
            "get_current_weather": get_current_weather,
            # Add more functions here as needed
        }

    def get_function(self, function_name):
        return self.functions.get(function_name)

    def register_function(self, function_name, function):
        self.functions[function_name] = function
