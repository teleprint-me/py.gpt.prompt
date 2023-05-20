# pygptprompt/chat.py
from typing import Optional

import prompt_toolkit
import tiktoken
from prompt_toolkit.history import FileHistory

from pygptprompt.command.factory import command_factory
from pygptprompt.context.config import get_api_key, get_configuration
from pygptprompt.context.session import (
    create_directory,
    get_session_name,
    load_session,
    save_session,
)
from pygptprompt.format import print_bold
from pygptprompt.openai import OpenAI
from pygptprompt.token import (
    get_token_count,
    get_token_limit,
    truncate_messages_for_token_limit,
)


class ChatContext:
    def __init__(self, config_path: Optional[str] = None):
        # Initialize settings
        # Configuration defaults to `./config.json`.
        self.config = get_configuration(config_path)
        # API Key defaults to `./.env`.
        self.api_key = get_api_key(self.config)
        # Sessions defaults to `./sessions` (defined in config)
        self.session_path = self.config.get("session_path", "sessions")
        # Setup OpenAI REST Interface
        self.openai: OpenAI = OpenAI(self.api_key)
        # Setup GPT Model settings
        self.model: str = self.config.get("model", "gpt-3.5-turbo")
        self.max_tokens: int = self.config.get("max_tokens", 1024)
        self.temperature: float = self.config.get("temperature", 0.5)

        # Initialize session
        create_directory(self.session_path)
        # NOTE: The user needs be prompted for the session name.
        # Ask the user to enter a session name or choose an existing one.
        self.session_name: str = get_session_name()
        self.messages: list[dict[str, str]] = load_session(self.session_name) or [
            self.config["system_message"]
        ]

        # Initialize model
        # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
        # gpt-4 context window: `upper_limit = 8192 - max_tokens`
        self.encoding: tiktoken.Encoding = tiktoken.encoding_for_model(self.model)
        self.upper_limit: int = get_token_limit(self.model, self.max_tokens)

    def print_message_history(self) -> None:
        # Print message history
        for message in self.messages:
            print()  # Add newline to pad output
            print_bold(message["role"])
            print(message["content"])
        print()  # Add newline to pad output

    def track_token_count(self) -> None:
        # Calculate the total number of tokens enqueued
        token_count: int = get_token_count(
            self.encoding.name,
            messages=self.messages,
        )

        # Output updated token count
        print(f"Consumed {token_count} tokens.\n")

    def prompt_user(self) -> bool:
        def prompt_continuation(width, line_number, is_soft_wrap):
            return ">" * width
            # Or: return [('', '>' * width)]

        try:
            print_bold("user")
            user_message: str = prompt_toolkit.prompt(
                "> ",
                multiline=True,
                prompt_continuation=prompt_continuation,
                history=FileHistory(f"sessions/{self.session_name}.history"),
            )
        except (KeyboardInterrupt, EOFError):
            # Auto save session on interrupt
            save_session(self.session_name, self.messages)
            exit()

        # Block and prompt user again if the input is empty
        if not user_message:
            return True

        # Allow user to save normally
        # if user_message in ["/save", "/s"]:
        #     save_session(self.session_name, self.messages)

        # Auto save and exit normally
        # if user_message in ["/quit", "/q", "/exit", "/e"]:
        #     save_session(self.session_name, self.messages)
        #     exit()

        # Handle user command
        if user_message.startswith("/"):
            command_response = command_factory(user_message)
            print(command_response)
            user_message = f"{user_message}\n{command_response}"

        # Add the user message to the conversation
        #   - Dequeue older messages to prevent overflow.
        #   - pop the second element to preserve the system prompt.
        self.messages = truncate_messages_for_token_limit(
            self.messages,
            {"role": "user", "content": user_message},
            self.upper_limit,
            self.encoding,
        )

        print()

        # Let the main loop continue
        return False

    def prompt_gpt(self) -> None:
        # Use a prompt to identify GPT's output
        print_bold("assistant")

        # Call the streaming API
        assistant_message = self.openai.stream_chat_completions(
            self.messages,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        # Handle command if assistant message starts with "/"
        if assistant_message:
            assistant_content = assistant_message["content"]
            if assistant_content.startswith("/"):
                print()  # pad with a newline to avoid mangling
                command_response = command_factory(assistant_content)
                print(command_response)
                assistant_content = f"{assistant_content}\n{command_response}"
                assistant_message = {"role": "assistant", "content": assistant_content}

            # Add the assistant message to the conversation
            self.messages = truncate_messages_for_token_limit(
                self.messages,
                assistant_message,
                self.upper_limit,
                self.encoding,
            )

        print("\n")  # pad output with newline characters

        # Save the updated messages to the session file
        save_session(self.session_name, self.messages)

    def loop(self) -> None:
        self.print_message_history()

        while True:
            self.track_token_count()

            # Handle user input
            if self.prompt_user():
                continue
            else:
                save_session(self.session_name, self.messages)

            # 4. Prompt model - Call custom streaming API
            self.prompt_gpt()
