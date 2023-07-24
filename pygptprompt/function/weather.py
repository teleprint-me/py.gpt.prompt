"""
pygptprompt/function/weather.py
"""
import requests


def get_current_weather(location: str, unit: str = "metric") -> str:
    """
    Get the current weather in a given location.
    Parameters:
    location (str): The city and state, e.g. San Francisco, CA
    unit (str): The unit system, can be either 'metric' or 'uscs'. Default is 'metric'.
    Returns:
    str: A string that describes the current weather.
    """

    # Replace spaces with hyphens and commas with underscores for the wttr.in URL
    location = location.replace(" ", "-").replace(",", "_")

    # Determine the unit query parameter
    unit_query = "m" if unit == "metric" else "u"
    # Set the API response formatting
    res_format = "%l+%T+%S+%s+%C+%w+%t"

    # Make a request to the wttr.in service
    response = requests.get(
        f"http://wttr.in/{location}?{unit_query}&format={res_format}"
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Return the weather report
        return response.text
    else:
        return f"Could not get the weather for {location}."
