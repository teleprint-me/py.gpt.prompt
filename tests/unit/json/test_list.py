"""
tests/unit/pattern/list.py
"""
from pygptprompt.json.list import JSONListTemplate
from pygptprompt.model.base import ChatModelResponse


class TestJSONListTemplate:
    def test_length(self, json_list_template, messages):
        assert json_list_template.length == len(messages)

    def test_data(self, json_list_template, messages):
        assert json_list_template.data == messages

    def test_append(
        self,
        json_list_template: JSONListTemplate,
        message: ChatModelResponse,
    ):
        initial_length = json_list_template.length
        json_list_template.append(message)
        assert json_list_template.length == initial_length + 1
        assert json_list_template.get(initial_length) == message

    def test_insert(
        self,
        json_list_template: JSONListTemplate,
        message: ChatModelResponse,
    ):
        initial_length = json_list_template.length
        index = 1
        json_list_template.insert(index, message)
        assert json_list_template.length == initial_length + 1
        assert json_list_template.get(index) == message
        assert json_list_template.insert(-1, message) is False
        assert json_list_template.insert(initial_length + 2, message) is False

    def test_get(self, json_list_template, messages):
        # Test getting elements at valid indices
        for index, message in enumerate(messages):
            assert json_list_template.get(index) == message

        # Test getting elements at invalid indices
        assert json_list_template.get(-1) is None
        assert json_list_template.get(len(messages)) is None

    def test_update(self, json_list_template, message):
        # Test updating elements at valid indices
        for index in range(json_list_template.length):
            assert json_list_template.update(index, message) is True
            assert json_list_template.get(index) == message

        # Test updating elements at invalid indices
        assert json_list_template.update(-1, message) is False
        assert json_list_template.update(json_list_template.length, message) is False

    def test_remove(self, json_list_template):
        # Test removing elements at valid indices
        for index in reversed(range(json_list_template.length)):
            assert json_list_template.remove(index) is True
            assert json_list_template.length == index

        # Verify all elements have been removed
        assert json_list_template.length == 0

        # Test removing elements at invalid indices
        assert json_list_template.remove(-1) is False
        assert json_list_template.remove(json_list_template.length) is False

    def test_pop(self, json_list_template, messages):
        assert json_list_template.length == 3
        message = json_list_template.pop(1)
        assert json_list_template.length == 2
        assert message is not None
        assert "role" in message and "content" in message
        assert message["role"] == "user"

    def test_clear(self, json_list_template):
        assert json_list_template.clear() is None
        assert json_list_template.data is None
