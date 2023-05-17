import os
from typing import Any

import tiktoken
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from tiktoken import Encoding

from pygptprompt.command.factory import command_factory
from pygptprompt.config import get_config
from pygptprompt.format import print_bold
from pygptprompt.openai import OpenAI
from pygptprompt.session import (
    create_sessions_directory,
    name_session,
    read_session,
    save_session,
)
from pygptprompt.token import (
    get_token_count,
    get_token_limit,
    truncate_messages_for_token_limit,
)

load_dotenv()

#
# TODO: Refactor to implement separation of concerns
#


def prompt_continuation(width, line_number, is_soft_wrap):
    return ">" * width
    # Or: return [('', '>' * width)]


def main():
    # Usage

    #
    # TODO: Prompt for configuration file path.
    #

    # Configuration defaults to `./config.json`.
    config: dict[str, Any] = get_config()
    max_tokens: int = config["max_tokens"]
    model: str = config["model"]
    temperature: float = config["temperature"]
    api_key: str = os.getenv("OPENAI_API_KEY") or ""
    openai: OpenAI = OpenAI(api_key)

    # Ask the user to enter a session name or choose an existing one
    create_sessions_directory()
    session_name: str = name_session()
    messages: list[dict[str, str]] = read_session(session_name) or [
        config["system_message"]
    ]

    # Print message history
    for message in messages:
        print()  # Add padding to command line
        print_bold(message["role"])
        print(message["content"])

    print()

    # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
    # gpt-4 context window: `upper_limit = 8192 - max_tokens`
    encoding: Encoding = tiktoken.encoding_for_model(model)
    upper_limit: int = get_token_limit(model, max_tokens)

    while True:
        # Calculate the total number of tokens enqueued
        token_count: int = get_token_count(encoding.name, messages=messages)
        print(f"Consumed {token_count} tokens.\n")

        # Ask the user for their message
        try:
            print_bold("user")
            user_message: str = prompt(
                "> ",
                multiline=True,
                prompt_continuation=prompt_continuation,
                history=FileHistory(f"sessions/{session_name}.history"),
            )
        except (KeyboardInterrupt, EOFError):
            save_session(session_name, messages)  # Auto save session
            exit()

        # Block and prompt user again if the input is empty
        if not user_message:
            continue

        #
        # TODO: Handle meta sessions
        #   - Allow user to manage sessions from within sessions
        #

        # Allow user to save normally
        if user_message in ["/save", "/s"]:
            save_session(session_name, messages)

        # Allow user to exit normally
        if user_message in ["/quit", "/q", "/exit", "/e"]:
            save_session(session_name, messages)  # Auto save session
            exit()

        # Handle user commands
        if user_message.startswith("/"):
            command_response = command_factory(user_message)
            print(command_response)
            user_message = f"{user_message}\n{command_response}"

        # Add the user message to the conversation
        #   - Dequeue older messages to prevent overflow.
        #   - pop the second element to preserve the system prompt.
        messages = truncate_messages_for_token_limit(
            messages,
            {"role": "user", "content": user_message},
            upper_limit,
            encoding,
        )

        print()

        # Use a prompt to identify GPT's output
        print_bold("assistant")

        # Call the streaming API
        assistant_message = openai.stream_chat_completions(
            messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
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
            messages = truncate_messages_for_token_limit(
                messages,
                assistant_message,
                upper_limit,
                encoding,
            )

        print("\n")  # output newline characters

        # Save the updated messages to the session file
        save_session(session_name, messages)


if __name__ == "__main__":
    main()
