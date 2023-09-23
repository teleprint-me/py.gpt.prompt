"""
pygptprompt/chat.py
"""
import sys
import traceback
from logging import Logger
from typing import Tuple

import click
from prompt_toolkit import prompt as input

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.model.sequence.context_manager import ContextWindowManager
from pygptprompt.model.sequence.transcript_manager import TranscriptManager
from pygptprompt.pattern.model import ChatModel, ChatModelResponse
from pygptprompt.storage.chroma import ChromaVectorStore


# NOTE:
# This is a sketch of the constructor for ChatSessionManager class.
def initialize_context_window(
    session_name: str,
    provider: str,
    config: ConfigurationManager,
    chat_model: ChatModel,
    vector_store: ChromaVectorStore,
    logger: Logger,
    embed: bool = False,
) -> Tuple[TranscriptManager, ContextWindowManager]:
    logger.debug("Initializing context window.")

    # Initialize System Prompt
    system_prompt = ChatModelResponse(
        role=config.get_value(f"{provider}.system_prompt.role"),
        content=config.get_value(f"{provider}.system_prompt.content"),
    )
    logger.debug("System prompt initialized.")

    # Paths
    context_manager_path = config.get_value("app.path.local") + "/context.json"
    transcript_manager_path = config.get_value("app.path.local") + "/transcript.json"
    logger.debug("Paths for context and transcript managers established.")

    # Initialize Managers
    context_window = ContextWindowManager(
        file_path=context_manager_path,
        provider=provider,
        config=config,
        chat_model=chat_model,
        vector_store=vector_store,
        embed=embed,
    )
    transcript_manager = TranscriptManager(
        file_path=transcript_manager_path,
        provider=provider,
        config=config,
        chat_model=chat_model,
    )
    logger.debug("Managers initialized.")

    # Load existing or start new session
    if context_window.load_to_chat_completions():
        context_window.logger.debug(
            f"Continuing previous session {session_name} from {context_manager_path}"
        )
    else:
        context_window.logger.debug(
            f"Starting new session {session_name} for {context_manager_path}"
        )
        context_window.enqueue(system_prompt)

    # Load transcript
    if transcript_manager.load_to_chat_completions():
        transcript_manager.logger.debug(
            f"Continuing previous session {session_name} from {transcript_manager_path}"
        )
    else:
        transcript_manager.logger.debug(
            f"Starting new session {session_name} for {transcript_manager_path}"
        )
        transcript_manager.enqueue(system_prompt)

    logger.debug("Context window initialized.")
    return transcript_manager, context_window


# NOTE:
# This is a sketch for managing the queue for the ChatSessionManager class.
def add_message_to_queue(
    new_message: ChatModelResponse,
    context_window: ContextWindowManager,
    transcript_manager: TranscriptManager,
    logger: Logger,
):
    # Append the new message to both context window and transcript
    logger.debug(f"{new_message['role'].upper()} Message: {new_message['content']}")
    context_window.enqueue(new_message)
    transcript_manager.enqueue(new_message)


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
@click.option(
    "--database_path",
    "-d",
    type=click.STRING,
    default="database",
    help="Path where embeddings are written to.",
)
def main(
    config_path,
    session_name,
    prompt,
    chat,
    embed,
    provider,
    database_path,
):
    if not (bool(prompt) ^ chat):
        print(
            "Use either --prompt or --chat, but not both.",
            "See --help for more information.",
        )
        sys.exit(1)

    session_name: str = session_name

    config = ConfigurationManager(config_path)

    logger: Logger = config.get_logger("app.log.general", "Chat", "DEBUG")
    logger.info(f"Using Session: {session_name}")
    logger.info(f"Using Config: {config_path}")
    logger.info(f"Using Prompt: {prompt}")
    logger.info(f"Using Chat: {chat}")
    logger.info(f"Using Embed: {embed}")
    logger.info(f"Using Provider: {provider}")
    logger.info(f"Using Database: {database_path}")

    function_factory = FunctionFactory(config)

    model_factory = ChatModelFactory(config)
    chat_model: ChatModel = model_factory.create_model(provider)

    # NOTE: Even though telemetry defaults to being off,
    # Chroma still (annoyingly) sets a UID in the home path.
    # Chroma will be deprecated in future releases simply because
    # it does not respect the end user.
    vector_store = ChromaVectorStore(
        collection_name=session_name,
        database_path=database_path,
        config=config,
        chat_model=chat_model,
    )

    transcript_manager, context_window = initialize_context_window(
        session_name=session_name,
        provider=provider,
        config=config,
        chat_model=chat_model,
        vector_store=vector_store,
        logger=logger,
        embed=embed,
    )

    print(context_window.system_message.get("role"))
    print(context_window.system_message.get("content"))
    print()

    try:
        if prompt:
            # Create a ChatModelResponse object for the user's prompt
            user_prompt = ChatModelResponse(role="user", content=prompt)

            # Log and add to context and transcript
            add_message_to_queue(
                new_message=user_prompt,
                context_window=context_window,
                transcript_manager=transcript_manager,
                logger=logger,
            )

            # Get assistant's response
            print("assistant")
            assistant_message = chat_model.get_chat_completion(
                messages=context_window.sequence
            )

            # Log and add to context and transcript
            add_message_to_queue(
                new_message=assistant_message,
                context_window=context_window,
                transcript_manager=transcript_manager,
                logger=logger,
            )

            print()  # DEBUG clutters CLI; This is temporary.
            context_window.save_from_chat_completions()
            transcript_manager.save_from_chat_completions()

            if embed:
                logger.debug(f"Chroma Heartbeat: {vector_store.get_chroma_heartbeat()}")
                logger.debug(
                    f"Chroma Collections: {vector_store.get_collection_count()}"
                )

        elif chat:
            # NOTE: Print previous content to stdout if it exists
            for message in context_window:
                # NOTE: We want to avoid outputting the function role
                # Maybe make this optional in the future?
                if message["role"] in ["user", "assistant"]:
                    print(message["role"])
                    print(message["content"])
                    print()

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

                add_message_to_queue(
                    new_message=user_message,
                    context_window=context_window,
                    transcript_manager=transcript_manager,
                    logger=logger,
                )

                # NOTE:
                # We don't want to duplicate user queries, so we skip saving
                # state here and wait until the end of the cycle to write.
                # If the script crashes, then the user message is lost.
                # This is a desirable behavior within the given context.

                print()  # Add padding to output
                print("assistant")

                # And for assistant output:
                assistant_message = chat_model.get_chat_completion(
                    messages=context_window.sequence
                )

                if assistant_message["role"] == "function":
                    # NOTE:
                    # Model responds to user query via function result

                    # 1. Query the function from the factory and execute it
                    function_result: ChatModelResponse = (
                        function_factory.execute_function(assistant_message)
                    )

                    # Check and skip if function result is None
                    if function_result is None:
                        logger.error(
                            f"Function {function_factory.function_name} did not return a result."
                        )
                        continue

                    # 2. Query the model using a prompt and function result
                    # NOTE: A prompt template is set by the user in the config
                    function_message: ChatModelResponse = (
                        function_factory.query_function(
                            chat_model=chat_model,
                            function_result=function_result,
                            messages=context_window.sequence,
                        )
                    )

                    # 3. We handle the return response as a "function message"
                    # We need to check and ensure everything went alright because
                    # query_function utilizes as a "shadow context window".
                    # The shadow context is a deepcopy of context window.
                    if function_message is not None:
                        add_message_to_queue(
                            new_message=function_message,
                            context_window=context_window,
                            transcript_manager=transcript_manager,
                            logger=logger,
                        )
                        context_window.enqueue(function_message)
                    else:
                        logger.error("Failed to generate a response message.")
                        continue
                else:  # NOTE: Keep an eye on this branch for buggy behavior
                    add_message_to_queue(
                        new_message=assistant_message,
                        context_window=context_window,
                        transcript_manager=transcript_manager,
                        logger=logger,
                    )

                # NOTE: We only write messages at the end of a cycle
                # The context, transcript, and embedding spaces are all isolated.
                # The context and transcript are written to JSON.
                # The embedding is written to a sqlite database.
                print()  # DEBUG clutters CLI; This is temporary.
                context_window.save_from_chat_completions()
                transcript_manager.save_from_chat_completions()

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
