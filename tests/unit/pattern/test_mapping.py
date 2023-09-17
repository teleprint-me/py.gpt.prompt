"""
tests/unit/pattern/mapping.py
"""


class TestMappingInterface:
    def test_create(self, map_template):
        # Create a new key-value pair
        assert map_template.create("new_key", "new_value") is True

        # Attempt to create the same key-value pair again (should return False since it already exists)
        assert map_template.create("new_key", "new_value") is False

        # Check existing key-value pair
        assert map_template.data["new_key"] == "new_value"

    def test_create_nested(self, map_template):
        assert map_template.create_nested("new_value", "nested", "key3") is True
        assert map_template.data["nested"]["key3"] == "new_value"

    def test_read(self, map_template):
        assert map_template.read("key1") == "value1"

    def test_read_nested(self, map_template):
        assert map_template.read_nested("nested", "key2") == "value2"

    def test_update(self, map_template):
        assert map_template.update("key1", "updated_value") is True
        assert map_template.data["key1"] == "updated_value"

    def test_update_nested(self, map_template):
        assert map_template.update_nested("updated_value", "nested", "key2") is True
        assert map_template.data["nested"]["key2"] == "updated_value"

    def test_delete(self, map_template):
        assert map_template.delete("key1") is True
        assert "key1" not in map_template.data

    def test_delete_nested(self, map_template):
        assert map_template.delete_nested("nested", "key2") is True
        assert "key2" not in map_template.data["nested"]

    def test_create_existing_key(self, map_template):
        assert map_template.create("key1", "new_value") is True
        assert (
            map_template.data["key1"] == "new_value"
        )  # ensure new old value no longer exists

    def test_read_nonexistent_key(self, map_template):
        assert map_template.read("nonexistent_key") is None

    def test_read_nested_nonexistent_key(self, map_template):
        assert map_template.read_nested("nested", "nonexistent_key") is None

    def test_update_and_create_behavior(self, map_template):
        # Update an existing key's value (should return True since the key exists)
        assert map_template.update("new_key", "updated_value") is True

        # Read the value to ensure it was updated
        assert map_template.read("new_key") == "updated_value"

        # Use update to create a new key-value pair (should return True since the key does not exist)
        assert map_template.update("nonexistent_key", "new_value") is True

        # Read the newly created value to ensure it was created
        assert map_template.read("nonexistent_key") == "new_value"

    def test_update_nested_nonexistent_key(self, map_template):
        assert (
            map_template.update_nested("new_value", "nested", "nonexistent_key")
            is False
        )

    def test_delete_nonexistent_key(self, map_template):
        assert map_template.delete("nonexistent_key") is True

    def test_delete_nested_nonexistent_key(self, map_template):
        assert map_template.delete_nested("nested", "nonexistent_key") is False

    def test_nested_operations_with_non_dict(self, map_template):
        assert map_template.read_nested("non_dict_key", "key") is None
        assert map_template.update_nested("new_value", "non_dict_key", "key") is False
        assert map_template.delete_nested("non_dict_key", "key") is False
