"""
tests/unit/test_config_path.py
"""
import os

from pygptprompt.config.path import evaluate_path


def test_evaluate_path():
    # Test with a path containing ~
    path = "~/test"
    expected = os.path.join(os.path.expanduser("~"), "test")
    assert evaluate_path(path) == expected

    # Test with a path containing an environment variable
    path = "$HOME/test"
    expected = os.path.join(os.environ["HOME"], "test")
    assert evaluate_path(path) == expected

    # Test with a path containing both ~ and an environment variable
    path = "~/$USER/test"
    expected = os.path.join(os.path.expanduser("~"), os.environ["USER"], "test")
    assert evaluate_path(path) == expected
