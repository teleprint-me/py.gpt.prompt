import os
import sys
from typing import List

import click
from huggingface_hub import hf_hub_download
from llama_cpp import ChatCompletionMessage, Llama

from pygptprompt import (
    DEFAULT_LOW_VRAM,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL_FILENAME,
    DEFAULT_MODEL_REPOSITORY,
    DEFAULT_N_BATCH,
    DEFAULT_N_CTX,
    DEFAULT_N_GPU_LAYERS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    logging,
)


def generate_response(llama_model, messages, max_tokens, temperature, top_p):
    content = ""
    response_generator = llama_model.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True,
    )

    print()  # Add padding between user input and assistant response
    print("assistant")
    sys.stdout.flush()
    for stream in response_generator:
        try:
            token = stream["choices"][0]["delta"]["content"]
            if token:
                print(token, end="")
                sys.stdout.flush()
                content += token
        except KeyError:
            continue
    print("\n")  # Add padding between user input and assistant response
    chat_completion = ChatCompletionMessage(
        role="assistant",
        content=content,
    )
    messages.append(chat_completion)
    return messages


@click.command()
@click.option(
    "--repo_id",
    type=click.STRING,
    default=DEFAULT_MODEL_REPOSITORY,
    help="The repository to download the model from. Default is TheBloke/orca_mini_7B-GGML.",
)
@click.option(
    "--filename",
    type=click.STRING,
    default=DEFAULT_MODEL_FILENAME,
    help="The filename of the model from the given repository. Default is orca-mini-7b.ggmlv3.q2_K.bin.",
)
@click.option(
    "--prompt",
    type=click.STRING,
    default=str(),
    help="Prompt the model with a string. Default: str",
)
@click.option(
    "--chat",
    type=click.BOOL,
    default=bool(),
    help="Enter a chat loop with the model. Default: False",
)
@click.option(
    "--n_ctx",
    type=click.INT,
    default=DEFAULT_N_CTX,
    help="Maximum context size. Default is 512.",
)
@click.option(
    "--n_batch",
    type=click.INT,
    default=DEFAULT_N_BATCH,
    help="Number of batches to use. Default is 512.",
)
@click.option(
    "--n_gpu_layers",
    type=click.INT,
    default=DEFAULT_N_GPU_LAYERS,
    help="Number of GPU layers to use. Default is 0.",
)
@click.option(
    "--low_vram",
    type=click.BOOL,
    default=DEFAULT_LOW_VRAM,
    help="Set to True if GPU device has low VRAM. Default is False.",
)
@click.option(
    "--max_tokens",
    type=click.INT,
    default=DEFAULT_MAX_TOKENS,
    help="The maximum number of tokens to generate. Default is 512.",
)
@click.option(
    "--temperature",
    type=click.FLOAT,
    default=DEFAULT_TEMPERATURE,
    help="The temperature to use for sampling. Default is 0.8.",
)
@click.option(
    "--top_p",
    type=click.FLOAT,
    default=DEFAULT_TOP_P,
    help="The top-p value to use for sampling. Default is 0.95.",
)
def main(
    repo_id,
    filename,
    n_ctx,
    n_batch,
    n_gpu_layers,
    low_vram,
    max_tokens,
    temperature,
    top_p,
    prompt,
    chat,
):
    cache_dir = os.path.join(
        os.path.expanduser("~"),
        ".cache",
        "huggingface",
        "hub",
    )

    logging.info(f"Using {repo_id} to load {filename}")

    try:
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            cache_dir=cache_dir,
        )
    except Exception as e:
        logging.error(f"Error downloading model: {e}")
        sys.exit(1)

    logging.info(f"Using {model_path} to load {repo_id} into memory")

    system_prompt = ChatCompletionMessage(
        role="system",
        content="My name is Orca. I am a helpful AI assistant.",
    )

    messages: List[ChatCompletionMessage] = [system_prompt]

    if prompt and chat:
        raise ValueError(
            "Use either --prompt or --chat, but not both."
        )  # NOTE: Only one option at a time!

    try:
        llama_model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            low_vram=low_vram,
            verbose=False,
        )

        logging.info("Generating response...")

        if prompt:
            # Add a single message to the list and generate a response
            user_prompt = ChatCompletionMessage(
                role="user",
                content=prompt,
            )
            messages.append(user_prompt)
            messages = generate_response(
                llama_model,
                messages,
                max_tokens,
                temperature,
                top_p,
            )

        elif chat:
            # Enter a chat loop
            while True:
                try:
                    print("user")
                    text_input = input("> ")
                except (EOFError, KeyboardInterrupt):
                    break

                user_prompt = ChatCompletionMessage(
                    role="user",
                    content=text_input,
                )
                messages.append(user_prompt)
                messages = generate_response(
                    llama_model,
                    messages,
                    max_tokens,
                    temperature,
                    top_p,
                )

    except Exception as e:
        logging.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
