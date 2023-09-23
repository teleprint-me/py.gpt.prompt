"""
pygptprompt/storage/sqlite.py
"""
import logging
from functools import wraps
from logging import Logger
from typing import List, Optional

from peewee import (
    CharField,
    DateTimeField,
    Model,
    OperationalError,
    SqliteDatabase,
    TextField,
)

from pygptprompt.pattern.logger import get_default_logger


def ensure_db_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.db.is_closed():
            logging.warning("Database connection is closed.")
            logging.info("Opening a new connection.")
            self.connect()
        return method(self, *args, **kwargs)

    return wrapper


def close_db_after_use(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        logging.info("Closing the database connection.")
        self.close()
        return result

    return wrapper


class SQLiteMemoryStore:
    def __init__(self, db_name: Optional[str] = None, logger: Optional[Logger] = None):
        self.db_name = db_name or "chat_model_static_memory.sqlite"
        self.db = SqliteDatabase(self.db_name)

        if logger:
            self._logger = logger
        else:
            self._logger = get_default_logger(self.__class__.__name__)

    def connect(self) -> bool:
        try:
            return self.db.connect()
        except OperationalError as message:
            self._logger.exception(message)
            self._logger.warning(f"Connection already exists: {self.db_name}")
        return False

    def close(self) -> bool:
        return self.db.close()

    def _create_chat_model_sequence(self, table_name: str) -> Model:
        # NOTE: A sequence can be the Context Window or Transcript
        db = self.db

        class ChatModelSequence(Model):
            role = CharField(index=True)
            content = TextField(null=True)
            function_call = TextField(null=True)
            function_args = TextField(null=True)
            user = CharField(null=True)
            timestamp = DateTimeField(index=True)

            class Meta:
                database = db
                db_table = f"sequence_{table_name}"

        return ChatModelSequence

    def _create_chat_model_memory(self, table_name: str) -> Model:
        # NOTE: A memory is a recorded fact about a person, place, thing, etc.
        db = self.db

        class ChatModelStaticMemory(Model):
            # NOTE: Keys need to be unique to avoid retrieval collisions
            key = CharField(index=True, unique=True)
            content = TextField()
            timestamp = DateTimeField(null=True, index=True)

            class Meta:
                database = db
                db_table = f"memory_{table_name}"

        return ChatModelStaticMemory

    def _create_model_by_type(self, model_id: str, table_name: str) -> Model:
        model_map = {
            "sequence": self._create_chat_model_sequence,
            "memory": self._create_chat_model_memory,
            # Add more models here as needed
        }

        if model_id not in model_map:
            raise ValueError(f"Unsupported model_id: {model_id}")

        return model_map[model_id](table_name)

    @ensure_db_connection
    def get_model(self, model_id: str, table_name: str) -> Model:
        model = self._create_model_by_type(model_id, table_name)

        if self.db.table_exists(model._meta.table_name):
            self._logger.info(f"Table {model._meta.table_name} already exists.")
        else:
            try:
                self.db.create_tables([model])
                self._logger.info(f"Table {model._meta.table_name} created.")
            except OperationalError as message:
                self._logger.exception(message)
                self._logger.warning(f"Table existence is ambiguous: {table_name}")

        return model

    @ensure_db_connection
    def get_models(self, model_id: str, table_names: List[str]) -> List[Model]:
        models = []
        new_models = []

        for table_name in table_names:
            model = self._create_model_by_type(model_id, table_name)
            models.append(model)

        for model in models:
            if self.db.table_exists(model._meta.table_name):
                new_models.append(model)
        try:
            if new_models:
                self.db.create_tables(new_models)
                self._logger.info(f"Tables for {new_models} created.")
        except OperationalError as message:
            self._logger.exception(message)
            self._logger.warning(f"Tables existence is ambiguous: {table_names}")

        return models
