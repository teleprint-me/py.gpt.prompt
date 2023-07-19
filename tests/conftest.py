"""
tests/conftest.py
"""
import os
from typing import Union

import pytest
from llama_cpp import ChatCompletionMessage

from pygptprompt.api.llama_cpp import LlamaCppAPI
from pygptprompt.api.openai import OpenAIAPI

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
def messages() -> list[ChatCompletionMessage]:
    return [
        ChatCompletionMessage(role="system", content="You are a helpful assistant."),
        ChatCompletionMessage(role="user", content="Who won the world series in 2020?"),
        ChatCompletionMessage(
            role="assistant",
            content="The Los Angeles Dodgers won the World Series in 2020.",
        ),
    ]


@pytest.fixture(scope="module")
def chat_completion() -> list[ChatCompletionMessage]:
    return [
        ChatCompletionMessage(role="system", content="You are a helpful assistant."),
        ChatCompletionMessage(
            role="user",
            content="Translate the following English text to French: 'The quick brown fox jumped over the lazy dog.'",
        ),
    ]


@pytest.fixture
def embedding_input() -> Union[str, list[str]]:
    return "This is a test sentence."


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
    return OpenAIAPI(api_key=config.get_api_key())


@pytest.fixture(scope="module")
def llama_cpp_api(config: ConfigurationManager) -> LlamaCppAPI:
    return LlamaCppAPI(
        repo_id=config.get_value("llama_cpp.model.repo_id"),
        filename=config.get_value("llama_cpp.model.filename"),
        n_ctx=config.get_value("llama_cpp.model.n_ctx"),
        n_batch=config.get_value("llama_cpp.model.n_batch"),
        n_gpu_layers=config.get_value("llama_cpp.model.n_gpu_layers"),
        low_vram=config.get_value("llama_cpp.model.low_vram"),
    )


# @pytest.fixture(scope="module")
# def session_token(config: ConfigurationManager) -> SessionToken:
#     return SessionToken(config)


# @pytest.fixture(scope="module")
# def session_model(config: ConfigurationManager) -> SessionModel:
#     return SessionModel(config)


# @pytest.fixture(scope="module")
# def session_policy(config):
#     return SessionPolicy(config)
