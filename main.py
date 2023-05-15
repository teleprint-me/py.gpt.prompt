import os

import tiktoken
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygptprompt.command import handle_command
from pygptprompt.openai import OpenAI

load_dotenv()


def prompt_continuation(width, line_number, is_soft_wrap):
    return "." * width
    # Or: return [('', '.' * width)]


def get_token_count(encoding_name: str, messages: list[dict[str, str]]) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    total_tokens = 0

    for message in messages:
        if "content" in message:
            string = message["content"]
            total_tokens += len(encoding.encode(string))

    return total_tokens


def main():
    # Usage
    max_tokens = 1024
    model = "gpt-3.5-turbo"
    api_key = os.getenv("OPENAI_API_KEY") or ""
    openai = OpenAI(api_key)

    # Initialize the conversation with a system message
    messages = [
        {
            "role": "system",
            "content": f"Your name is {model}. You are a pair programming assistant. You have access to special commands. Use `/help` for more information. You and the User are both allowed to execute commands listed in the `/help` output.",
        }
    ]

    # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
    # gpt-4 context window: `upper_limit = 8192 - max_tokens`
    encoding = tiktoken.encoding_for_model(model)
    if model == "gpt-3.5-turbo":
        upper_limit = 4096 - max_tokens
    else:
        upper_limit = 8192 - max_tokens

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

        # Enqueue the user message to the conversation
        messages.append({"role": "user", "content": user_message})

        # Dequeue older messages to prevent overflow.
        #   - pop the second element to preserve the system prompt.
        while token_count >= upper_limit:
            messages.pop(1)

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

            # Enqueue the assistant message.
            messages.append(assistant_message)

        print("\n")  # output newline characters


if __name__ == "__main__":
    main()
