"""
tests/conftest.py
"""
import os
from typing import List, Union

import pytest
from llama_cpp import ChatCompletionMessage

from pygptprompt.api.factory import ChatModelFactory
from pygptprompt.api.llama_cpp import LlamaCppAPI
from pygptprompt.api.openai import OpenAIAPI
from pygptprompt.api.types import ExtendedChatCompletionMessage
from pygptprompt.config.json import read_json

# from pygptprompt.session.model import SessionModel
# from pygptprompt.session.policy import SessionPolicy
# from pygptprompt.session.token import SessionToken
from pygptprompt.config.manager import ConfigurationManager


def pytest_addoption(parser):
    parser.addoption(
        "--private",
        action="store_true",
        default=False,
        help="test private endpoints",
    )
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="run slow tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "private: test private endpoints")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--private"):
        # --no-skip given: do not skip tests
        return
    private = pytest.mark.skip(reason="need --private option to run")
    for item in items:
        if "private" in item.keywords:
            item.add_marker(private)


@pytest.fixture(scope="module")
def message() -> ChatCompletionMessage:
    return ChatCompletionMessage(
        role="user",
        content="How many cards are there in a single deck of cards?",
    )


@pytest.fixture(scope="module")
def messages() -> List[ChatCompletionMessage]:
    return [
        ChatCompletionMessage(role="system", content="You are a helpful assistant."),
        ChatCompletionMessage(role="user", content="Who won the world series in 2020?"),
        ChatCompletionMessage(
            role="assistant",
            content="The Los Angeles Dodgers won the World Series in 2020.",
        ),
    ]


@pytest.fixture(scope="module")
def chat_completion() -> List[ChatCompletionMessage]:
    return [
        ChatCompletionMessage(role="system", content="You are a helpful assistant."),
        ChatCompletionMessage(
            role="user",
            content="Translate the following English text to French: 'The quick brown fox jumped over the lazy dog.'",
        ),
    ]


@pytest.fixture(scope="module")
def function_completion() -> List[ExtendedChatCompletionMessage]:
    return [
        ExtendedChatCompletionMessage(
            role="system", content="You are a helpful assistant."
        ),
        ExtendedChatCompletionMessage(
            role="user", content="What's the weather like in San Francisco, CA?"
        ),
    ]


@pytest.fixture
def mock_weather_callback() -> object:
    """
    A mock function for getting the current weather.
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

    return get_current_weather


@pytest.fixture
def embedding_input() -> Union[str, List[str]]:
    return "This is a test sentence."


@pytest.fixture(scope="module")
def json_config() -> dict:
    return read_json("tests/config.sample.json")


@pytest.fixture(scope="module")
def json_filepath(tmpdir_factory) -> str:
    return str(tmpdir_factory.mktemp("data").join("test.json"))


@pytest.fixture(scope="module")
def config_file_path() -> str:
    if os.path.exists("config.json"):
        filepath = "config.json"
    else:
        filepath = "tests/config.sample.json"
    return filepath


@pytest.fixture(scope="module")
def config(config_file_path: str) -> ConfigurationManager:
    return ConfigurationManager(file_path=config_file_path)


@pytest.fixture(scope="module")
def openai_api(config: ConfigurationManager) -> OpenAIAPI:
    return OpenAIAPI(config=config)


@pytest.fixture(scope="module")
def llama_cpp_api(config: ConfigurationManager) -> LlamaCppAPI:
    return LlamaCppAPI(config=config)


@pytest.fixture(scope="module")
def chat_model_factory(config: ConfigurationManager):
    return ChatModelFactory(config)


# @pytest.fixture(scope="module")
# def session_token(config: ConfigurationManager) -> SessionToken:
#     return SessionToken(config)


# @pytest.fixture(scope="module")
# def session_model(config: ConfigurationManager) -> SessionModel:
#     return SessionModel(config)


# @pytest.fixture(scope="module")
# def session_policy(config):
#     return SessionPolicy(config)
