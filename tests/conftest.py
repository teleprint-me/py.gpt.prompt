# tests/conftest.py
import os

import pytest

from pygptprompt.chat.token import ChatToken
from pygptprompt.openai import OpenAI
from pygptprompt.setting import GlobalConfiguration


def pytest_addoption(parser):
    parser.addoption(
        "--private",
        action="store_true",
        default=False,
        help="test private endpoints",
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
def messages():
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Translate the following English text to French: 'The quick brown fox jumped over the lazy dog.'",
        },
    ]


@pytest.fixture(scope="module")
def dialog():
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {
            "role": "assistant",
            "content": "The Los Angeles Dodgers won the World Series in 2020.",
        },
    ]


@pytest.fixture(scope="module")
def config_filepath() -> str:
    if os.path.exists("config.json"):
        filepath = "config.json"
    else:
        filepath = "tests/config.sample.json"
    return filepath


@pytest.fixture(scope="module")
def config(config_filepath: str) -> GlobalConfiguration:
    return GlobalConfiguration(config_filepath)


@pytest.fixture(scope="module")
def chat_token(config: GlobalConfiguration) -> ChatToken:
    return ChatToken(config)


@pytest.fixture(scope="module")
def openai(config: GlobalConfiguration) -> OpenAI:
    return OpenAI(config.get_api_key())
