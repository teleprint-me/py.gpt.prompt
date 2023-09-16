"""
pygptprompt/chat.py
"""
import sys
from datetime import datetime
from logging import Logger

import click
from chromadb import API, PersistentClient, Settings
from chromadb.api.models.Collection import Collection
from prompt_toolkit import prompt as input

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.pattern.list import ListTemplate
from pygptprompt.pattern.model import (
    ChatModel,
    ChatModelEmbeddingFunction,
    ChatModelResponse,
)


@click.command()
@click.argument(
    "session_name",
    type=click.STRING,
    default="default",
)
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
    "--embed",
    is_flag=True,
    help="Employ the chroma vector database while prompting or chatting.",
)
@click.option(
    "--provider",
    type=click.STRING,
    default="llama_cpp",
    help="Specify the model provider to use. Options are 'openai' for GPT models and 'llama_cpp' for Llama models.",
)
@click.option(
    "--path_database",
    type=click.STRING,
    default="database",
    help="The path the embeddings are written to.",
)
def main(session_name, config_path, prompt, chat, embed, provider, path_database):
    if not (bool(prompt) ^ chat):
        print(
            "Use either --prompt or --chat, but not both.",
            "See --help for more information.",
        )
        sys.exit(1)

    session_name: str = session_name

    config: ConfigurationManager = ConfigurationManager(config_path)
    logger: Logger = config.get_logger("app.log.general", "Chat", "DEBUG")

    function_factory = FunctionFactory(config)
    model_factory: ChatModelFactory = ChatModelFactory(config)
    chat_model: ChatModel = model_factory.create_model(provider)

    embedding_function: ChatModelEmbeddingFunction = ChatModelEmbeddingFunction(
        model=chat_model
    )

    # Uses PostHog library to collect telemetry
    chroma_client: API = PersistentClient(
        path=path_database,
        settings=Settings(anonymized_telemetry=False),
    )

    try:
        collection: Collection = chroma_client.create_collection(
            name=session_name, embedding_function=embedding_function
        )
        logger.info(f"Created collection {session_name}")
    except ValueError:
        collection: Collection = chroma_client.get_collection(
            name=session_name, embedding_function=embedding_function
        )
        logger.info(f"Loaded collection {session_name}")

    def initialize_list_template(
        file_path: str,
        system_prompt: ChatModelResponse,
        session_name: str,
        logger: Logger,
    ) -> ListTemplate:
        list_template = ListTemplate(file_path=file_path)
        list_template.make_directory()

        if list_template.load_json():
            logger.info(f"Continuing previous session {session_name} from {file_path}")
        else:
            logger.info(f"Starting new session {session_name} for {file_path}")
            list_template.append(system_prompt)

        return list_template

    # Initialize ListTemplates for Context and Transcript
    system_prompt = ChatModelResponse(
        role=config.get_value(f"{provider}.system_prompt.role"),
        content=config.get_value(f"{provider}.system_prompt.content"),
    )

    context_manager_path = config.get_value("app.path.local") + "/context.json"
    transcript_manager_path = config.get_value("app.path.local") + "/transcript.json"

    context_window = initialize_list_template(
        context_manager_path, system_prompt, "context", logger
    )
    transcript = initialize_list_template(
        transcript_manager_path, system_prompt, "transcript", logger
    )

    try:
        print(system_prompt.get("role"))
        print(system_prompt.get("content"))
        print()

        if prompt:
            # Create a ChatModelResponse object for the user's prompt
            user_prompt = ChatModelResponse(role="user", content=prompt)

            # Log and add to context and transcript
            logger.info(f"User Prompt: {user_prompt.content}")
            context_window.append(user_prompt)
            transcript.append(user_prompt)

            # Get assistant's response
            assistant_message = chat_model.get_chat_completion(
                messages=context_window.data
            )

            # Log and add to context and transcript
            logger.info(f"Assistant Message: {assistant_message.content}")

            context_window.append(assistant_message)
            context_window.save_from_chat_completions()

            transcript.append(assistant_message)
            transcript.save_from_chat_completions()

        elif chat:
            # Extract the common logic to a function
            def add_message_to_db(collection, session_name, message):
                unique_id = f"{session_name}_{datetime.utcnow().isoformat()}"
                collection.add(
                    documents=[message["content"]],
                    metadatas=[{"role": message["role"]}],
                    ids=[unique_id],
                )

            while True:
                # Manage user message
                try:
                    print("user")
                    text_input = input(
                        "> ", multiline=True, wrap_lines=True, prompt_continuation=". "
                    )
                except (EOFError, KeyboardInterrupt):
                    break

                user_message = ChatModelResponse(role="user", content=text_input)
                context_window.append(user_message)
                transcript.append(user_message)

                if embed:
                    add_message_to_db(collection, session_name, user_message)

                # NOTE: We don't want to duplicate user queries, so we skip saving state here.

                # Manage assistant message
                print()  # Add padding to output
                print("assistant")

                assistant_message = chat_model.get_chat_completion(
                    messages=context_window.data
                )

                if assistant_message["role"] == "function":
                    # Query the function from the factory and execute it
                    result: ChatModelResponse = function_factory.execute_function(
                        assistant_message
                    )
                    # Skip to user prompt if result is None
                    if result is None:
                        logger.error(
                            f"Function {function_factory.function_name} did not return a result."
                        )
                        continue

                    message: ChatModelResponse = function_factory.query_function(
                        chat_model=chat_model,
                        result=result,
                        messages=context_window.data,
                    )

                    if message is not None:
                        context_window.append(message)
                    else:
                        logger.error("Failed to generate a response message.")
                        continue

                context_window.append(assistant_message)
                transcript.append(assistant_message)

                if embed:
                    add_message_to_db(collection, session_name, assistant_message)

                context_window.save_from_chat_completions()
                transcript.save_from_chat_completions()

                print()  # Add padding to output
                print(f"Heartbeat: {chroma_client.heartbeat()}")
                print(f"Collections: {collection.count()}")
                print()  # Add padding to output
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
