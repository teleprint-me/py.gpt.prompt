# NOTE: This is just a prototype to work out the details of interacting with
# the chat completions API using the `stream` flag while set to `True`.
# This will be the basis for the C++ port of this implementation.
import json
import os
import sys

import requests
import tiktoken
from dotenv import load_dotenv
from prompt_toolkit import prompt as input

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


class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.chat_completions_url = "https://api.openai.com/v1/chat/completions"

    def stream_chat_completions(
        self,
        messages,
        model="gpt-3.5-turbo",
        max_tokens=512,
        temperature=0.7,
    ):
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,  # Enable REST API streaming
            "messages": messages,
        }

        response = requests.post(
            self.chat_completions_url,
            headers=self.headers,
            json=data,
            stream=True,  # Enable HTTP token streaming
        )

        if response.status_code == 200:
            message = ""
            # Iterate over the response data one line at a time
            for line in response.iter_lines():
                # If the line is not empty
                if line:
                    # Decode it to string
                    line = line.decode("utf-8")

                    # Check if the line starts with 'data: '
                    if line.startswith("data: "):
                        # If it does, strip it out
                        line = line[6:]

                    # If the line is '[DONE]', stop processing
                    if line == "[DONE]":
                        break

                    json_line = json.loads(line)

                    # Aggregate and flush the tokens to output
                    try:
                        token = json_line["choices"][0]["delta"]["content"]
                        if token:
                            message += token
                            print(token, end="")
                            sys.stdout.flush()
                    except (KeyError,):
                        continue

            # Return the assistant's message after the loop
            return {"role": "assistant", "content": message}
        else:
            print(f"Error: {response.status_code}")
            print(f"Error message: {response.text}")
            return None  # Return None in case of an error


def main():
    # Usage
    max_tokens = 1024
    model = "gpt-3.5-turbo"
    api_key = os.getenv("OPENAI_API_KEY")
    openai = OpenAI(api_key)

    # Initialize the conversation with a system message
    messages = [
        {
            "role": "system",
            "content": "Your name is GPT. You are a helpful assistant.",
        }
    ]

    while True:
        # Ask the user for their message
        try:
            user_message = input(
                "You: ",
                multiline=True,
                prompt_continuation=prompt_continuation,
            )
        except (KeyboardInterrupt, EOFError):
            exit()

        # Block and prompt user again if the input is empty
        if not user_message:
            continue

        # Allow user to exit normally
        if user_message == "quit":
            exit()

        # Enqueue the user message to the conversation
        messages.append({"role": "user", "content": user_message})

        # Use a prompt to identify GPT's output
        print("\nGPT:", end=" ")

        # Call the streaming API
        assistant_message = openai.stream_chat_completions(
            messages,
            model=model,
            max_tokens=max_tokens,
        )

        # Enqueue the assistant message.
        if assistant_message is not None:
            messages.append(assistant_message)

        print("\n")  # output newline characters

        # Calculate the total number of tokens enqueued
        encoding = tiktoken.encoding_for_model(model)
        token_count = get_token_count(encoding.name, messages=messages)
        print(f"Consumed {token_count} tokens.\n")

        # gpt-3.5-turbo context window: `upper_limit = 4096 - max_tokens`
        # gpt-4 context window: `upper_limit = 8192 - max_tokens`
        if model == "gpt-3.5-turbo":
            upper_limit = 4096 - max_tokens
        else:
            upper_limit = 8192 - max_tokens

        # Dequeue messages to prevent overflow
        #   - pop the second element to preserve the system prompt.
        while token_count >= upper_limit:
            messages.pop(1)


if __name__ == "__main__":
    main()
