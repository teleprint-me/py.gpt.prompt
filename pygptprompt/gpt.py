import sys
from typing import List

import click
from llama_cpp import ChatCompletionMessage
from prompt_toolkit import prompt as input

from pygptprompt import logging
from pygptprompt.api.openai import OpenAIAPI
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
def main(config_path, prompt, chat):
    if not (bool(prompt) ^ chat):
        print(
            "Use either --prompt or --chat, but not both.",
            "See --help for more information.",
        )
        sys.exit(1)

    config = ConfigurationManager(config_path)

    openai = OpenAIAPI(config=config)

    system_prompt = ChatCompletionMessage(
        role=config.get_value("openai.system_prompt.role"),
        content=config.get_value("openai.system_prompt.content"),
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
            message: ChatCompletionMessage = openai.get_chat_completions(
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
                message: ChatCompletionMessage = openai.get_chat_completions(
                    messages=messages,
                )
                print()
                messages.append(message)

        else:
            print("Nothing to do.")
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
