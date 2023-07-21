import sys
from typing import Iterator, List

import openai
from llama_cpp import ChatCompletionChunk, ChatCompletionMessage

from pygptprompt import logging
from pygptprompt.config.manager import ConfigurationManager

config = ConfigurationManager("tests/config.sample.json")

openai.api_key = config.get_api_key()


def get_current_weather(location: str, unit: str = "celsius"):
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


def stream_chat_completion(
    self, response_generator: Iterator[ChatCompletionChunk]
) -> ChatCompletionMessage:
    """
    Process the stream of chat completion chunks and return the generated message.

    Args:
        response_generator (Iterator[ChatCompletionChunk]): The chat completion chunk stream.

    Returns:
        ChatCompletionMessage: The generated message.
    """
    content = ""

    for stream in response_generator:
        try:
            token = stream["choices"][0]["delta"]["content"]
            if token:
                print(token, end="")
                sys.stdout.flush()
                content += token
        except KeyError:
            continue

    print()  # Add newline to model output
    sys.stdout.flush()

    return ChatCompletionMessage(role="assistant", content=content)


def get_chat_completions(
    self,
    messages: List[ChatCompletionMessage],
) -> ChatCompletionMessage:
    """
    Generate chat completions using the OpenAI language models.

    Args:
        messages (List[ChatCompletionMessage]): The list of chat completion messages.

    Returns:
        ChatCompletionMessage: The generated chat completion message.
    """
    if not messages:
        raise KeyError("Messages is a required argument.")

    try:
        # Call the OpenAI API's /v1/chat/completions endpoint
        response = openai.ChatCompletion.create(
            messages=messages,
            functions=config.get_value("function.definitions"),
            function_call=config.get_value("function.call"),
            model=config.get_value("openai.chat_completions.model", "gpt-3.5-turbo"),
            temperature=config.get_value("openai.chat_completions.temperature", 0.8),
            max_tokens=config.get_value("openai.chat_completions.max_tokens", 1024),
            top_p=config.get_value("openai.chat_completions.top_p", 0.95),
            n=config.get_value("openai.chat_completions.n", 1),
            stop=config.get_value("openai.chat_completions.stop", []),
            presence_penalty=config.get_value(
                "openai.chat_completions.presence_penalty", 0
            ),
            frequency_penalty=config.get_value(
                "openai.chat_completions.frequency_penalty", 0
            ),
            logit_bias=config.get_value("openai.chat_completions.logit_bias", {}),
            stream=True,  # NOTE: Always coerce streaming
        )
        return stream_chat_completion(response)
    except Exception as e:
        logging.error(f"Error generating chat completions: {e}")
        return ChatCompletionMessage(role="error", content=str(e))
