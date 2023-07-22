import json
import sys
from typing import Iterator, List, Tuple

import openai
from llama_cpp import ChatCompletionChunk
from prompt_toolkit import prompt as input

from pygptprompt import logging
from pygptprompt.api.types import ExtendedChatCompletionMessage
from pygptprompt.config.manager import ConfigurationManager

config = ConfigurationManager("tests/config.sample.json")

openai.api_key = config.get_api_key()


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


def extract_content(delta: dict, content: str) -> str:
    if delta and "content" in delta and delta["content"]:
        token = delta["content"]
        print(token, end="")
        sys.stdout.flush()
        content += token
    return content


def extract_function_call(
    delta: dict, function_call_name: str, function_call_args: str
) -> Tuple[str, str]:
    if delta and "function_call" in delta and delta["function_call"]:
        function_call = delta["function_call"]
        if not function_call_name:
            function_call_name = function_call.get("name", "")
        function_call_args += str(function_call.get("arguments", ""))
    return function_call_name, function_call_args


def handle_finish_reason(
    finish_reason: str, function_call_name: str, function_call_args: str, content: str
) -> ExtendedChatCompletionMessage:
    if finish_reason:
        if finish_reason == "function_call":
            return ExtendedChatCompletionMessage(
                role="function",
                function_call=function_call_name,
                function_args=function_call_args,
            )
        elif finish_reason == "stop":
            print()  # Add newline to model output
            sys.stdout.flush()
            return ExtendedChatCompletionMessage(role="assistant", content=content)
        else:
            # Handle unexpected finish_reason
            raise ValueError(f"Warning: Unexpected finish_reason '{finish_reason}'")


def stream_chat_completion(
    response_generator: Iterator[ChatCompletionChunk],
) -> ExtendedChatCompletionMessage:
    function_call_name = None
    function_call_args = ""
    content = ""

    for chunk in response_generator:
        delta = chunk["choices"][0]["delta"]
        content = extract_content(delta, content)
        function_call_name, function_call_args = extract_function_call(
            delta, function_call_name, function_call_args
        )
        finish_reason = chunk["choices"][0]["finish_reason"]
        message = handle_finish_reason(
            finish_reason, function_call_name, function_call_args, content
        )

        if message:
            return message


def get_chat_completions(
    messages: List[ExtendedChatCompletionMessage],
) -> ExtendedChatCompletionMessage:
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
        return ExtendedChatCompletionMessage(role="error", content=str(e))


if __name__ == "__main__":
    messages: List[ExtendedChatCompletionMessage] = [
        ExtendedChatCompletionMessage(
            role="system", content="My name is ChatGPT. I am a helpful assistant."
        )
    ]

    while True:
        try:
            print("user")
            user_input = input(
                "> ",
                multiline=True,
                wrap_lines=True,
                prompt_continuation=". ",
            )
            print()
            messages.append(
                ExtendedChatCompletionMessage(
                    role="user",
                    content=user_input,
                )
            )
        except (EOFError, KeyboardInterrupt):
            exit()

        print("assistant")
        assistant_message = get_chat_completions(messages)
        print()
        if assistant_message["role"] == "function":
            function_name = assistant_message["function_call"]
            function_args = json.loads(assistant_message["function_args"])
            logging.info(
                f"{config.get_value('openai.chat_completions.model')}: using {function_name}"
            )
            if function_name == "get_current_weather":
                response = get_current_weather(**function_args)
                messages.append(
                    ExtendedChatCompletionMessage(
                        role="assistant",
                        content=response,
                    )
                )
                print(response)
                print()
            else:
                logging.error(f"Unknown function: {function_name}")
        else:
            logging.info(f"ChatGPT: {assistant_message['content']}")
            messages.append(assistant_message)
