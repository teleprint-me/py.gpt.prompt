"""
tests/conftest.py
"""
import json
import os
from typing import List, Union

import pytest

from pygptprompt.config.json import read_json
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.model.llama_cpp import LlamaCppModel
from pygptprompt.model.openai import OpenAIModel
from pygptprompt.pattern.json import JSONTemplate
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.mapping import MappingTemplate
from pygptprompt.pattern.model import ChatModel, ChatModelChatCompletion

# from pygptprompt.session.model import SessionModel
# from pygptprompt.session.policy import SessionPolicy
# from pygptprompt.session.token import ChatSessionTokenManager


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


@pytest.fixture
def encoding_input() -> Union[str, List[str]]:
    return "This is a test sentence."


@pytest.fixture
def embedding_input() -> Union[str, List[str]]:
    return "This is a test sentence."


@pytest.fixture(scope="module")
def message() -> ChatModelChatCompletion:
    return ChatModelChatCompletion(
        role="user",
        content="How many cards are there in a single deck of cards?",
    )


@pytest.fixture(scope="module")
def messages() -> List[ChatModelChatCompletion]:
    return [
        ChatModelChatCompletion(role="system", content="You are a helpful assistant."),
        ChatModelChatCompletion(
            role="user", content="Who won the world series in 2020?"
        ),
        ChatModelChatCompletion(
            role="assistant",
            content="The Los Angeles Dodgers won the World Series in 2020.",
        ),
    ]


@pytest.fixture(scope="module")
def chat_completion() -> List[ChatModelChatCompletion]:
    return [
        ChatModelChatCompletion(role="system", content="You are a helpful assistant."),
        ChatModelChatCompletion(
            role="user",
            content="Translate the following English text to French: 'The quick brown fox jumped over the lazy dog.'",
        ),
    ]


@pytest.fixture(scope="module")
def function_completion() -> List[ChatModelChatCompletion]:
    return [
        ChatModelChatCompletion(role="system", content="You are a helpful assistant."),
        ChatModelChatCompletion(
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

        Returns:
            str: A string that describes the current weather.
        NOTE:
            This is a mock function, so let's return a mock weather report.
        """
        return f"The current weather in {location} is 20 degrees {unit}."

    return get_current_weather


@pytest.fixture(scope="module")
def temp_json_path() -> str:
    return "tests/test.temp.json"


@pytest.fixture(scope="module")
def temp_json_backup_path() -> str:
    return "tests/test.temp.backup.json"


@pytest.fixture(scope="module")
def temp_json_nested_path() -> str:
    return "tests/nested/test.temp.json"


@pytest.fixture(scope="module")
def temp_json_data() -> dict:
    return {"test": "data"}


@pytest.fixture
def temp_json_file(temp_json_path, temp_json_data):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(temp_json_path), exist_ok=True)

    # Write the temp data to the file
    with open(temp_json_path, "w") as f:
        json.dump(temp_json_data, f)

    yield temp_json_path

    # Cleanup the temporary file after the test
    os.remove(temp_json_path)


@pytest.fixture(scope="module")
def json_template(temp_json_path: str, temp_json_data: dict) -> JSONTemplate:
    return JSONTemplate(temp_json_path, temp_json_data)


@pytest.fixture(scope="module")
def json_template_nested(
    temp_json_nested_path: str, temp_json_data: dict
) -> JSONTemplate:
    return JSONTemplate(temp_json_nested_path, temp_json_data)


@pytest.fixture(scope="module")
def config_file_path() -> str:
    if os.path.exists("config.json"):
        return "config.json"
    return "tests/config.sample.json"


@pytest.fixture(scope="module")
def config_json(config_file_path: str) -> dict:
    return read_json(config_file_path)


@pytest.fixture(scope="module")
def map_template(config_json: dict) -> MappingTemplate:
    return MappingTemplate(config_json)


@pytest.fixture(scope="module")
def list_template(messages: List[ChatModelChatCompletion]) -> ListTemplate:
    return ListTemplate(messages)


@pytest.fixture(scope="module")
def config(config_file_path: str) -> ConfigurationManager:
    return ConfigurationManager(config_file_path)


@pytest.fixture(scope="module")
def openai_model(config: ConfigurationManager) -> OpenAIModel:
    return OpenAIModel(config=config)


@pytest.fixture(scope="module")
def llama_cpp_model(config: ConfigurationManager) -> LlamaCppModel:
    return LlamaCppModel(config=config)


@pytest.fixture(scope="module")
def chat_model_factory(config: ConfigurationManager):
    return ChatModelFactory(config=config)


@pytest.fixture(scope="module")
def chat_model(chat_model_factory: ChatModelFactory) -> ChatModel:
    return chat_model_factory.create_model(provider="llama_cpp")


# @pytest.fixture(scope="module")
# def chat_session_token_manager(
#     config: ConfigurationManager, chat_model: ChatModel
# ) -> ChatSessionTokenManager:
#     return ChatSessionTokenManager(
#         provider="llama_cpp", config=config, model=chat_model
#     )


# @pytest.fixture(scope="module")
# def session_model(config: ConfigurationManager) -> SessionModel:
#     return SessionModel(config)


# @pytest.fixture(scope="module")
# def session_policy(config):
#     return SessionPolicy(config)
