"""
pygptprompt/function/weather.py
"""


def get_current_weather(location: str, unit: str = "celsius") -> str:
    """
    Get the current weather in a given location.
    Parameters:
    location (str): The city and state, e.g. San Francisco, CA
    unit (str): The unit of temperature, can be either 'celsius' or 'fahrenheit'. Default is 'celsius'.
    Returns:
    str: A string that describes the current weather.
    """

    # This is a mock function, so let's return a mock weather report.
    weather_report = f"The current weather in {location} is 20 degrees {unit}."
    return weather_report
