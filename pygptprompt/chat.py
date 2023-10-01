"""
pygptprompt/chat.py
"""
import sys
import traceback
from logging import Logger
from pathlib import Path

import click
from prompt_toolkit import prompt as input

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.function.manager import FunctionManager
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.model.sequence.session_manager import SessionManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse
from pygptprompt.storage.chroma import ChromaVectorStore


@click.command()
@click.argument(
    "config_path",
    type=click.Path(exists=True),
)
@click.option(
    "--session_name",
    "-s",
    type=click.STRING,
    default="default",
    help="Label for the database collection and associated JSON files.",
)
@click.option(
    "--prompt",
    "-v",
    type=click.STRING,
    default="",
    help="Prompt the model with a string.",
)
@click.option(
    "--chat",
    "-x",
    is_flag=True,
    help="Enter a chat loop with the model.",
)
@click.option(
    "--embed",
    "-e",
    is_flag=True,
    help="Use the chroma vector database while prompting or chatting.",
)
@click.option(
    "--provider",
    "-p",
    type=click.STRING,
    default="llama_cpp",
    help="Specify the model provider to use. Options are 'openai' for GPT models and 'llama_cpp' for Llama models.",
)
def main(
    config_path,
    session_name,
    prompt,
    chat,
    embed,
    provider,
):
    if not (bool(prompt) ^ chat):
        print(
            "Use either --prompt or --chat, but not both.",
            "See --help for more information.",
        )
        sys.exit(1)

    session_name: str = session_name

    config = ConfigurationManager(config_path)

    logger: Logger = config.get_logger("general", Path(__file__).stem)
    logger.info(f"Using Session: {session_name}")
    logger.info(f"Using Config: {config_path}")
    logger.info(f"Using Prompt: {prompt}")
    logger.info(f"Using Chat: {chat}")
    logger.info(f"Using Embed: {embed}")
    logger.info(f"Using Provider: {provider}")

    model_factory = ChatModelFactory(config)
    chat_model: ChatModel = model_factory.create_model(provider)

    function_factory = FunctionFactory(config)
    function_manager = FunctionManager(function_factory, config, chat_model)

    # NOTE: Even though telemetry defaults to being off,
    # Chroma still (annoyingly) sets a UID in the home path.
    # Chroma will be deprecated in future releases simply because
    # it does not respect the end user.
    if embed:
        vector_store = ChromaVectorStore(
            collection_name=session_name,
            config=config,
            chat_model=chat_model,
        )
    else:
        vector_store = None

    # Initialize System Prompt
    system_prompt = ChatModelResponse(
        role=config.get_value(f"{provider}.system_prompt.role"),
        content=config.get_value(f"{provider}.system_prompt.content"),
    )

    session_manager = SessionManager(
        session_name=session_name,
        provider=provider,
        config=config,
        chat_model=chat_model,
        vector_store=vector_store,
    )

    session_manager.load(system_prompt=system_prompt)

    try:
        if prompt:
            # Create a ChatModelResponse object for the user's prompt
            user_message = ChatModelResponse(role="user", content=prompt)

            # Log and add to context and transcript
            session_manager.enqueue(message=user_message)

            # NOTE:
            # We don't want to duplicate user queries, so we skip saving
            # state here and wait until the assistant responds.
            # If the script crashes, then the user message is lost.
            # This is a desirable behavior within the given context.

            # Get assistant's response
            print("assistant")

            # And for assistant output:
            assistant_message = chat_model.get_chat_completion(
                messages=session_manager.output()
            )

            if assistant_message["role"] == "function":
                function_manager.process_function(assistant_message, session_manager)
            else:
                session_manager.enqueue(message=assistant_message)

            # NOTE: We only write messages after the assistants response.
            # The context, transcript, and embedding spaces are encapsulated.
            # The context and transcript are written to JSON.
            # The embeddings are written to sqlite database.
            session_manager.save()

            if embed:
                print()  # Add padding to output
                logger.debug(f"Chroma Heartbeat: {vector_store.get_chroma_heartbeat()}")
                logger.debug(
                    f"Chroma Collections: {vector_store.get_collection_count()}"
                )

        elif chat:
            # NOTE: Print previous content to stdout if it exists
            session_manager.print()

            while True:
                # Manage user message
                try:
                    print("user")
                    text_input = input(
                        "> ", multiline=True, wrap_lines=True, prompt_continuation=". "
                    )
                except (EOFError, KeyboardInterrupt):
                    break

                # Then, in your chat loop for user input:
                user_message = ChatModelResponse(role="user", content=text_input)

                session_manager.enqueue(message=user_message)

                # NOTE:
                # We don't want to duplicate user queries, so we skip saving
                # state here and wait until the end of the cycle to write.
                # If the script crashes, then the user message is lost.
                # This is a desirable behavior within the given context.

                print()  # Add padding to output
                print("assistant")

                # And for assistant output:
                assistant_message = chat_model.get_chat_completion(
                    messages=session_manager.output()
                )

                if assistant_message["role"] == "function":
                    function_manager.process_function(
                        assistant_message, session_manager
                    )
                else:
                    session_manager.enqueue(message=assistant_message)

                # NOTE: We only write messages at the end of a cycle
                # The context, transcript, and embedding spaces are encapsulated.
                # The context and transcript are written to JSON.
                # The embeddings are written to sqlite database.
                session_manager.save()

                if embed:
                    print()  # Add padding to output
                    logger.debug(
                        f"Chroma Heartbeat: {vector_store.get_chroma_heartbeat()}"
                    )
                    logger.debug(
                        f"Chroma Collections: {vector_store.get_collection_count()}"
                    )

                print()  # Add padding to output
    except Exception as e:
        print()  # Add padding to output
        logger.error(f"Error generating response: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
