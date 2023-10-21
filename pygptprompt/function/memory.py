"""
pygptprompt/function/memory.py
"""
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.chroma import ChromaVectorFunction
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.function.sqlite import SQLiteMemoryFunction
from pygptprompt.pattern.model import ChatModel
from pygptprompt.storage.chroma import ChromaVectorStore

episodic_function_definitions = [
    {
        "name": "ChromaVectorFunction_query_collection",
        "description": "Query the collection for documents.",
        "parameters": {
            "type": "object",
            "properties": {
                "query_texts": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}},
                    ]
                },
                "n_results": {"type": "integer"},
                "where": {"type": "object"},
                "where_document": {"type": "object"},
                "include": {
                    "type": "array",
                    "items": {"enum": ["metadatas", "documents", "distances"]},
                },
            },
            "required": ["query_texts"],
        },
    },
    {
        "name": "ChromaVectorFunction_upsert_to_collection",
        "description": "Upsert documents to the collection.",
        "parameters": {
            "type": "object",
            "properties": {
                "ids": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}},
                    ]
                },
                "metadatas": {
                    "oneOf": [
                        {"type": "object", "additionalProperties": {"type": "string"}},
                        {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": {"type": "string"},
                            },
                        },
                    ]
                },
                "documents": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "array", "items": {"type": "string"}},
                    ]
                },
            },
            "required": ["ids", "metadatas", "documents"],
        },
    },
    {
        "name": "SQLiteMemoryFunction_get_all_keys",
        "description": "Retrieve all the keys from the memory records in the database.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "SQLiteMemoryFunction_query_memory",
        "description": "Query a memory record with a given key from the database.",
        "parameters": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    },
    {
        "name": "SQLiteMemoryFunction_update_memory",
        "description": "Update or create a memory record with a given key and content in the database.",
        "parameters": {
            "type": "object",
            "properties": {"key": {"type": "string"}, "content": {"type": "string"}},
            "required": ["key", "content"],
        },
    },
    {
        "name": "SQLiteMemoryFunction_delete_memory",
        "description": "Delete a memory record with a given key from the database.",
        "parameters": {
            "type": "object",
            "properties": {"key": {"type": "string"}},
            "required": ["key"],
        },
    },
]


class AugmentedMemoryManager:
    def __init__(
        self,
        function_factory: FunctionFactory,
        config: ConfigurationManager,
        chat_model: ChatModel,
    ):
        self.function_factory = function_factory
        self.config = config
        self.chat_model = chat_model

    def _register_sqlite_memory(self, table_name: str) -> None:
        self.function_factory.register_class(
            "SQLiteMemoryFunction",
            SQLiteMemoryFunction,
            table_name=table_name,
            config=self.config,
        )
        self.function_factory.map_class_methods(
            "SQLiteMemoryFunction",
            ["get_all_keys", "query_memory", "update_memory", "delete_memory"],
        )

    def _register_vector_memory(self, table_name: str) -> None:
        self.function_factory.register_class(
            "ChromaVectorFunction",
            ChromaVectorFunction,
            collection_name=table_name,
            config=self.config,
            chat_model=self.chat_model,
        )
        self.function_factory.map_class_methods(
            "ChromaVectorFunction", ["query_collection", "upsert_to_collection"]
        )

    def _create_vector_memory(self, table_name: str) -> ChromaVectorStore:
        return ChromaVectorStore(
            collection_name=table_name,
            config=self.config,
            chat_model=self.chat_model,
        )

    def register_episodic_memory(self, table_name: str) -> ChromaVectorStore:
        self._register_sqlite_memory(table_name)
        self._register_vector_memory(table_name)
        return self._create_vector_memory(table_name)

    def register_episodic_functions(self) -> bool:
        functions = self.config.get_value("function.definitions", [])
        functions.extend(episodic_function_definitions)
        return self.config.set_value("function.definitions", functions)
