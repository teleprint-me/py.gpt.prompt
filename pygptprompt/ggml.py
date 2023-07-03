import sys
from typing import List

import click
from llama_cpp import ChatCompletionMessage
from prompt_toolkit import prompt as input

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
from pygptprompt.api.ggml.requests import LlamaCppRequests, LlamaResponse


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
    help="The filename of the model from the given repository. Default is orca-mini-7b.ggmlv3.q5_1.bin.",
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
    llama_requests = LlamaCppRequests(
        repo_id=repo_id,
        filename=filename,
        n_ctx=n_ctx,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        low_vram=low_vram,
        verbose=False,
    )

    system_prompt = ChatCompletionMessage(
        role="system",
        content="My name is Orca. I am a helpful AI assistant.",
    )

    messages: List[ChatCompletionMessage] = [system_prompt]

    if not prompt and not chat:
        raise ValueError(
            "Neither prompt nor chat were provided. "
            "Did you forget to set the options value?"
        )

    if prompt and chat:
        raise ValueError(
            "Use either --prompt or --chat, but not both."
        )  # NOTE: Only one option at a time!

    try:
        print(system_prompt.get("role"))
        print(system_prompt.get("content"))
        print()

        if prompt:
            # Add a single message to the list and generate a response
            user_prompt = ChatCompletionMessage(
                role="user",
                content=prompt,
            )
            messages.append(user_prompt)
            print("assistant")
            llama_response: LlamaResponse = llama_requests.get(
                endpoint="chat_completions",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                stream=True,
            )
            messages.append(llama_response)

        elif chat:
            # Enter a chat loop
            while True:
                try:
                    print("user")
                    text_input = input(
                        "> ",
                        multiline=True,
                        wrap_lines=True,
                        prompt_continuation=". ",
                    )
                except (EOFError, KeyboardInterrupt):
                    break
                user_message = ChatCompletionMessage(
                    role="user",
                    content=text_input,
                )
                messages.append(user_message)

                print()
                print("assistant")
                llama_response: LlamaResponse = llama_requests.get(
                    endpoint="chat_completions",
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    stream=True,
                )
                print()
                messages.append(llama_response)
        else:
            print("Nothing to do.")
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
