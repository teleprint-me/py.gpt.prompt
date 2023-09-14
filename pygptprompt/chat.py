"""
pygptprompt/chat.py
"""
import sys
from datetime import datetime
from typing import List

import click
from chromadb import API, PersistentClient, Settings
from chromadb.api.models.Collection import Collection
from chromadb.api.types import Documents, QueryResult
from prompt_toolkit import prompt as input

from pygptprompt import logging
from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.function.factory import FunctionFactory
from pygptprompt.model.factory import ChatModelFactory
from pygptprompt.pattern.model import (
    ChatModel,
    ChatModelChatCompletion,
    ChatModelEmbeddingFunction,
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
        logging.info(f"Created collection {session_name}")
    except ValueError:
        collection: Collection = chroma_client.get_collection(
            name=session_name, embedding_function=embedding_function
        )
        logging.info(f"Loaded collection {session_name}")

    system_prompt = ChatModelChatCompletion(
        role=config.get_value(f"{provider}.system_prompt.role"),
        content=config.get_value(f"{provider}.system_prompt.content"),
    )

    messages: List[ChatModelChatCompletion] = [system_prompt]

    try:
        print(system_prompt.get("role"))
        print(system_prompt.get("content"))
        print()

        if prompt:
            user_prompt = ChatModelChatCompletion(role="user", content=prompt)
            messages.append(user_prompt)
            print("assistant")
            message: ChatModelChatCompletion = chat_model.get_chat_completion(
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
                user_message = ChatModelChatCompletion(role="user", content=text_input)
                messages.append(user_message)

                print()
                print("assistant")
                message: ChatModelChatCompletion = chat_model.get_chat_completion(
                    messages=messages,
                )

                if message["role"] == "function":
                    # Query the function from the factory and execute it
                    result: ChatModelChatCompletion = function_factory.execute_function(
                        message
                    )
                    # Skip to user prompt if result is None
                    if result is None:
                        logging.error(
                            f"Function {function_factory.function_name} did not return a result."
                        )
                        continue

                    message: ChatModelChatCompletion = function_factory.query_function(
                        chat_model=chat_model, result=result, messages=messages
                    )

                    if message is not None:
                        messages.append(message)
                    else:
                        logging.error("Failed to generate a response message.")
                        continue

                print()
                messages.append(message)

        elif embed:
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
                user_message = ChatModelChatCompletion(role="user", content=text_input)
                messages.append(user_message)
                add_message_to_db(collection, session_name, chat_model, user_message)
                print()  # Add padding to output

                # Manage assistant message
                print("assistant")
                message: ChatModelChatCompletion = chat_model.get_chat_completion(
                    messages=messages,
                )

                if message["role"] == "function":
                    # Query the function from the factory and execute it
                    result: ChatModelChatCompletion = function_factory.execute_function(
                        message
                    )
                    # Skip to user prompt if result is None
                    if result is None:
                        logging.error(
                            f"Function {function_factory.function_name} did not return a result."
                        )
                        continue

                    message: ChatModelChatCompletion = function_factory.query_function(
                        chat_model=chat_model, result=result, messages=messages
                    )

                    if message is not None:
                        messages.append(message)
                    else:
                        logging.error("Failed to generate a response message.")
                        continue

                print()  # Add padding to output
                messages.append(message)
                add_message_to_db(collection, session_name, chat_model, message)

                print(f"Heartbeat: {chroma_client.heartbeat()}")
                print(f"Collections: {collection.count()}")
                print()  # Add padding to output
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
