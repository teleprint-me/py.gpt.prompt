# tests/conftest.py
import os

import pytest

from pygptprompt.config import Configuration


def pytest_addoption(parser):
    parser.addoption(
        "--private", action="store_true", default=False, help="test private endpoints"
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
def config_filepath() -> str:
    if os.path.exists("config.json"):
        filepath = "config.json"
    else:
        filepath = "tests/config.sample.json"
    return filepath


@pytest.fixture(scope="module")
def config(config_filepath: str) -> Configuration:
    return Configuration(config_filepath)
