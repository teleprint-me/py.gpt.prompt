"""
pygptprompt/cli/chat.py

"The way we intuitively think about things is just not the way the world is. Maybe some day cognitive science will reach the level of physics, in 19th century, and recognize that our intuitive concept of the world isn't the way it works."
    - Noam Chomsky, MLST - On the Critique of Connections and Cognitive Architecture
"""

import os
import sys
import traceback
from logging import Logger
from pathlib import Path

import click
import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from rich.markdown import Markdown
from rich.panel import Panel

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.function.manager import FunctionManager
from pygptprompt.function.memory import AugmentedMemoryManager
from pygptprompt.model.base import ChatModel, ChatModelResponse
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.model.sequence.session_manager import SessionManager


def sweep_console(text: str) -> int:
    """
    Removes the specified text from the console by estimating its line coverage
    and moving the cursor up to 'sweep' these lines from view.

    Args:
        text (str): The text to be removed from the console.

    Returns:
        int: The estimated number of lines swept from the console.
    """
    # Get the terminal width to estimate line wraps
    terminal_width, _ = os.get_terminal_size()
    total_lines_to_sweep = 1  # Start with 1 for the initial line
    lines = text.split("\n")

    # Calculate the total lines to sweep, including wrapped lines
    for line in lines:
        line_wraps = (len(line) // terminal_width) + 1
        total_lines_to_sweep += line_wraps

    # Use ANSI escape codes to move cursor up and clear lines
    for _ in range(total_lines_to_sweep):
        # Move cursor up and return to start of line without deleting
        print("\x1b[A", end="\r", flush=True)

    return total_lines_to_sweep


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
)
@click.option(
    "--session",
    "-s",
    type=click.STRING,
    default="default",
    help="Specify a session label for the database collection and JSON files.",
)
@click.option(
    "--input",
    "-i",
    type=click.STRING,
    default="",
    help="Provide a prompt text for the model.",
)
@click.option(
    "--chat",
    "-c",
    is_flag=True,
    help="Enter an interactive chat session with the model.",
)
@click.option(
    "--memory",
    "-m",
    is_flag=True,
    help="Enable augmented episodic memory mode while interacting.",
)
@click.option(
    "--provider",
    "-p",
    type=click.STRING,
    default="llama_cpp",
    help="Specify the model provider ('openai' or 'llama_cpp').",
)
def main(
    config_path,
    session,
    input,
    chat,
    memory,
    provider,
):
    if not (bool(input) ^ chat):
        print(
            "Use either --input or --chat, but not both.",
            "See --help for more information.",
        )
        sys.exit(1)

    config = ConfigurationManager(config_path)

    logger: Logger = config.get_logger("general", Path(__file__).stem)
    logger.info(f"Using Session: {session}")
    logger.info(f"Using Config: {config_path}")
    logger.info(f"Using Prompt: {input}")
    logger.info(f"Using Chat: {chat}")
    logger.info(f"Using Embed: {memory}")
    logger.info(f"Using Provider: {provider}")

    model_factory = ChatModelFactory(config)
    chat_model: ChatModel = model_factory.create_model(provider)

    function_factory = FunctionFactory(config)
    function_manager = FunctionManager(function_factory, config, chat_model)

    vector_store = None

    if memory:
        memory_manager = AugmentedMemoryManager(function_factory, config, chat_model)
        if memory_manager.register_episodic_functions():
            vector_store = memory_manager.register_episodic_memory(session)

    # Initialize System Prompt
    system_prompt = ChatModelResponse(
        role=config.get_value(f"{provider}.system_prompt.role"),
        content=config.get_value(f"{provider}.system_prompt.content"),
    )

    session_manager = SessionManager(
        session_name=session,
        provider=provider,
        config=config,
        chat_model=chat_model,
        vector_store=vector_store,
    )

    session_manager.load(system_prompt=system_prompt)

    try:
        if input:
            # Create a ChatModelResponse object for the user's input
            user_message = ChatModelResponse(role="user", content=input)

            # Log and add to context and transcript
            session_manager.enqueue(message=user_message)

            # NOTE:
            # We don't want to duplicate user queries, so we skip saving
            # state here and wait until the assistant responds.
            # If the script crashes, then the user message is lost.
            # This is a desirable behavior within the given context.

            # Get assistant's response
            assistant_message = chat_model.get_chat_completion(
                messages=session_manager.output()
            )

            if "function_call" in assistant_message:
                function_manager.process_function(assistant_message, session_manager)
            else:
                session_manager.enqueue(assistant_message)

            # NOTE: We only write messages after the assistants response.
            # The context, transcript, and embedding spaces are encapsulated.
            # The context and transcript are written to JSON.
            # The embeddings are written to sqlite database.
            session_manager.save()

            if memory:
                print()  # Add padding to output
                logger.debug(f"Chroma Heartbeat: {vector_store.get_chroma_heartbeat()}")
                logger.debug(
                    f"Chroma Collections: {vector_store.get_collection_count()}"
                )

        elif chat:
            # NOTE: Print previous content to stdout if it exists
            session_manager.print(["system", "user", "assistant", "function"])
            auto_suggest = AutoSuggestFromHistory()
            cache_path = f"{config.evaluate_path('app.cache')}/{session}.history"
            session = PromptSession(history=FileHistory(cache_path))

            while True:
                # Manage user message
                try:
                    user_content = session.prompt(
                        "Prompt: ⌥ + ⏎ | Copy: ⌘ + s (a|s) | Exit: ⌘ + c:\n",
                        multiline=True,
                        auto_suggest=auto_suggest,
                        # key_bindings=key_bindings,  # TODO
                    ).strip()
                except (EOFError, KeyboardInterrupt):
                    break

                # Clean up and sweep console for user input
                sweep_console(user_content)
                # Make user input look pretty
                panel = Panel(Markdown(user_content), title="user", title_align="left")
                chat_model.console.print(panel)

                # prepare user input for chat model:
                user_message = ChatModelResponse(role="user", content=user_content)
                session_manager.enqueue(message=user_message)

                # NOTE:
                # We don't want to duplicate user queries, so we skip saving
                # state here and wait until the end of the cycle to write.
                # If the script crashes, then the user message is lost.
                # This is a desirable behavior within the given context.

                # Get assistant's response
                assistant_message = chat_model.get_chat_completion(
                    messages=session_manager.output()
                )

                if "function_call" in assistant_message:
                    function_manager.process_function(
                        assistant_message, session_manager
                    )
                else:
                    session_manager.enqueue(assistant_message)

                print()  # pad assistant output.
                if memory:
                    logger.debug(
                        f"Chroma Heartbeat: {vector_store.get_chroma_heartbeat()}"
                    )
                    logger.debug(
                        f"Chroma Collections: {vector_store.get_collection_count()}"
                    )
                session_manager.print_token_count()
                # NOTE: We only write messages at the end of a cycle
                # The context, transcript, and embedding spaces are encapsulated.
                # The context and transcript are written to JSON.
                # The embeddings are written to sqlite database.
                session_manager.save()
    except Exception as e:
        print()  # Add padding to output
        logger.error(f"Error generating response: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
