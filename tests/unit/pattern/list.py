"""
tests/unit/pattern/list.py
"""
from typing import List

from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import ChatModelResponse


class TestListTemplate:
    def test_length(self, list_template, messages):
        assert list_template.length == len(messages)

    def test_data(self, list_template, messages):
        assert list_template.data == messages

    def test_append(
        self,
        list_template: ListTemplate,
        message: ChatModelResponse,
    ):
        initial_length = list_template.length
        list_template.append(message)
        assert list_template.length == initial_length + 1
        assert list_template.get(initial_length) == message

    def test_insert(
        self,
        list_template: ListTemplate,
        message: ChatModelResponse,
    ):
        initial_length = list_template.length
        index = 1
        list_template.insert(index, message)
        assert list_template.length == initial_length + 1
        assert list_template.get(index) == message
        assert list_template.insert(-1, message) is False
        assert list_template.insert(initial_length + 2, message) is False

    def test_get(self, list_template, messages):
        # Test getting elements at valid indices
        for index, message in enumerate(messages):
            assert list_template.get(index) == message

        # Test getting elements at invalid indices
        assert list_template.get(-1) is None
        assert list_template.get(len(messages)) is None

    def test_update(self, list_template, message):
        # Test updating elements at valid indices
        for index in range(list_template.length):
            assert list_template.update(index, message) is True
            assert list_template.get(index) == message

        # Test updating elements at invalid indices
        assert list_template.update(-1, message) is False
        assert list_template.update(list_template.length, message) is False

    def test_remove(self, list_template):
        # Test removing elements at valid indices
        for index in reversed(range(list_template.length)):
            assert list_template.remove(index) is True
            assert list_template.length == index

        # Verify all elements have been removed
        assert list_template.length == 0

        # Test removing elements at invalid indices
        assert list_template.remove(-1) is False
        assert list_template.remove(list_template.length) is False

    def test_pop(self, list_template, messages):
        assert list_template.length == 3
        message = list_template.pop(1)
        assert list_template.length == 2
        assert message is not None
        assert "role" in message and "content" in message
        assert message["role"] == "user"

    def test_clear(self, list_template):
        assert list_template.clear() is None
        assert list_template.data is None
