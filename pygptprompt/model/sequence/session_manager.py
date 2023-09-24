"""
pygptprompt/model/sequence/session_manager.py
"""
from typing import Optional, Tuple

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.model.sequence.context_manager import ContextWindowManager
from pygptprompt.model.sequence.transcript_manager import TranscriptManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse
from pygptprompt.storage.chroma import ChromaVectorStore


class SessionManager:
    def __init__(
        self,
        session_name: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
        vector_store: Optional[ChromaVectorStore] = None,
    ):
        self.session_name = session_name
        self.provider = provider
        self.config = config
        self.chat_model = chat_model
        self.logger = self.config.get_logger("app.log.general", self.__class__.__name__)
        self.context_window = None
        self.transcript = None

    def create_managers(
        self,
        session_name: str,
        provider: str,
        config: ConfigurationManager,
        chat_model: ChatModel,
        vector_store: Optional[ChromaVectorStore] = None,
    ) -> Tuple[ContextWindowManager, TranscriptManager]:
        common_args = {
            "file_path": f"{config.get_value('app.path.local')}/{session_name}_{{}}.json",
            "provider": provider,
            "config": config,
            "chat_model": chat_model,
            "vector_store": vector_store,
        }

        context_window = ContextWindowManager(
            **{
                **common_args,
                "file_path": common_args["file_path"].format("context"),
            }
        )

        transcript = TranscriptManager(
            **{
                **common_args,
                "file_path": common_args["file_path"].format("transcript"),
            }
        )

        return context_window, transcript

    def _initialize_managers(self, system_prompt):
        self.context_window, self.transcript = self.create_managers(
            self.session_name,
            self.provider,
            self.config,
            self.chat_model,
            self.vector_store,
        )

        # Load or Start new session
        if (
            self.context_window.load_to_chat_completions()
            and self.transcript.load_to_chat_completions()
        ):
            self.logger.debug(f"Continuing previous session {self.session_name}")
        else:
            self.logger.debug(f"Starting new session {self.session_name}")
            self.context_window.enqueue(system_prompt)
            self.transcript.enqueue(system_prompt)

    def load(self, system_prompt: ChatModelResponse) -> None:
        self._initialize_managers(system_prompt=system_prompt)

    def save(self) -> bool:
        return (
            self.context_window.save_from_chat_completions()
            and self.transcript.save_from_chat_completions()
        )

    def enqueue(self, message: ChatModelResponse) -> None:
        self.context_window.enqueue(message=message)
        self.transcript.enqueue(message=message)

    def dequeue(self) -> ChatModelResponse:
        return self.context_window.dequeue()

    def output(self) -> None:
        # NOTE: Print previous content to stdout if it exists
        for message in self.context_window:
            # NOTE: We want to avoid outputting the function role
            # Maybe make this optional in the future?
            if message["role"] in ["user", "assistant"]:
                print(message["role"])
                print(message["content"])
                print()
