import os

import tiktoken
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygptprompt.command import config, handle_command
from pygptprompt.openai import OpenAI
from pygptprompt.token import (
    get_token_count,
    get_token_limit,
    truncate_messages_for_token_limit,
)

load_dotenv()


def prompt_continuation(width, line_number, is_soft_wrap):
    return "." * width
    # Or: return [('', '.' * width)]


def main():
    # Usage
    max_tokens: int = config["max_tokens"]
    model: str = config["model"]
    api_key: str = os.getenv("OPENAI_API_KEY") or ""
    openai = OpenAI(api_key)

    # Initialize the conversation with a system message
    messages: list[dict[str, str]] = [config["system_message"]]

    # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
    # gpt-4 context window: `upper_limit = 8192 - max_tokens`
    encoding, upper_limit = get_token_limit(model, max_tokens)

    while True:
        # Calculate the total number of tokens enqueued
        token_count = get_token_count(encoding.name, messages=messages)
        print(f"Consumed {token_count} tokens.\n")

        # Ask the user for their message
        try:
            user_message = prompt(
                "You: ",
                multiline=True,
                prompt_continuation=prompt_continuation,
                history=FileHistory("sessions/.prompt_history"),
            )
        except (KeyboardInterrupt, EOFError):
            exit()

        # Block and prompt user again if the input is empty
        if not user_message:
            continue

        # Allow user to exit normally
        if user_message == "quit":
            exit()

        if user_message.startswith("/"):
            command_response = handle_command(user_message)
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

        # Use a prompt to identify GPT's output
        print("\nGPT:", end=" ")

        # Call the streaming API
        assistant_message = openai.stream_chat_completions(
            messages,
            model=model,
            max_tokens=max_tokens,
        )

        # Handle command if assistant message starts with "/"
        if assistant_message is not None:
            assistant_content = assistant_message["content"]
            if assistant_content.startswith("/"):
                command_response = handle_command(assistant_content)
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


if __name__ == "__main__":
    main()
