"""
pygptprompt/function/factory.py
"""

from pygptprompt.function.weather import get_current_weather

FUNCTION_REGISTRY = {
    "get_current_weather": get_current_weather,
    # Add more functions here as needed
}
