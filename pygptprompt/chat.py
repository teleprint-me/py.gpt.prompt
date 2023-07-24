"""
pygptprompt/chat.py
"""
import copy
import sys
from typing import List

import click
from llama_cpp import ChatCompletionMessage
from prompt_toolkit import prompt as input

from pygptprompt import logging
from pygptprompt.api.factory import ChatModel, ChatModelFactory
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory


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
    function_factory = FunctionFactory(config)

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
                    # Query the function from the factory and execute it
                    result: ChatCompletionMessage = function_factory.query_function(
                        message
                    )
                    # Skip to user prompt if result is None
                    if result is None:
                        logging.error(
                            f"Function {function_factory.function_name} did not return a result."
                        )
                        continue

                    prompt_template: str = ""

                    # Make a copy of the current message list
                    shadow_messages = copy.deepcopy(messages)
                    # Append the function response message to the shadow context
                    shadow_messages.append(result)
                    # Get the prompt template from the configuration file
                    prompt_templates: list[dict[str, str]] = config.get_value(
                        "function.templates", []
                    )

                    for template in prompt_templates:
                        if template.get("name", "") == function_factory.function_name:
                            prompt_template = template.get("prompt", "")

                    if not prompt_template:
                        logging.error(
                            f"Failed to retrieve prompt template for {function_factory.function_name}"
                        )
                        continue

                    # Create a new ChatCompletionMessage with the prompt template
                    prompt_message = ChatCompletionMessage(
                        role="user", content=prompt_template
                    )
                    # Add the prompt message to the shadow context
                    shadow_messages.append(prompt_message)
                    # Get the assistant's response to the prompt
                    message = model.get_chat_completions(
                        messages=shadow_messages,
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
