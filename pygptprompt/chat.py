"""
pygptprompt/chat.py
"""
import json
import sys
from typing import List

import click
from llama_cpp import ChatCompletionMessage
from prompt_toolkit import prompt as input

from pygptprompt import logging
from pygptprompt.api.factory import ChatModel, ChatModelFactory
from pygptprompt.config.manager import ConfigurationManager


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
    default="config.json",
)
@click.option(
    "--prompt",
    type=click.STRING,
    default=str(),
    help="Prompt the model with a string.",
)
@click.option(
    "--chat",
    is_flag=True,
    help="Enter a chat loop with the model.",
)
@click.option(
    "--provider",
    type=click.STRING,
    default="llama_cpp",
    help="Specify the model provider to use. Options are 'openai' for GPT models and 'llama_cpp' for Llama models.",
)
def main(config_path, prompt, chat, provider):
    if not (bool(prompt) ^ chat):
        print(
            "Use either --prompt or --chat, but not both.",
            "See --help for more information.",
        )
        sys.exit(1)

    config: ConfigurationManager = ConfigurationManager(config_path)

    factory: ChatModelFactory = ChatModelFactory(config)
    model: ChatModel = factory.create_model(provider)

    system_prompt = ChatCompletionMessage(
        role=config.get_value(f"{provider}.system_prompt.role"),
        content=config.get_value(f"{provider}.system_prompt.content"),
    )

    messages: List[ChatCompletionMessage] = [system_prompt]

    try:
        print(system_prompt.get("role"))
        print(system_prompt.get("content"))
        print()

        if prompt:
            user_prompt = ChatCompletionMessage(role="user", content=prompt)
            messages.append(user_prompt)
            print("assistant")
            message: ChatCompletionMessage = model.get_chat_completions(
                messages=messages,
            )
            messages.append(message)

        elif chat:
            while True:
                try:
                    print("user")
                    text_input = input(
                        "> ", multiline=True, wrap_lines=True, prompt_continuation=". "
                    )
                except (EOFError, KeyboardInterrupt):
                    break
                user_message = ChatCompletionMessage(role="user", content=text_input)
                messages.append(user_message)

                print()
                print("assistant")
                message: ChatCompletionMessage = model.get_chat_completions(
                    messages=messages,
                )

                if message["role"] == "function":
                    # Extract the function name and arguments
                    function_name = message["function_call"]
                    function_args = json.loads(message["function_args"])

                    # Call the function
                    result = getattr(model, function_name)(**function_args)

                    # Print the result
                    print(result)
                else:
                    # Print the message as usual
                    print(message["content"])
                print()
                messages.append(message)

        else:
            print("Nothing to do.")
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
