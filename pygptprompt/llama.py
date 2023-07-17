import sys
from typing import List

import click
from llama_cpp import ChatCompletionMessage, EmbeddingData
from prompt_toolkit import prompt as input

from pygptprompt import (
    GGML_FILENAME,
    GGML_LOW_VRAM,
    GGML_MAX_TOKENS,
    GGML_N_BATCH,
    GGML_N_CTX,
    GGML_N_GPU_LAYERS,
    GGML_REPO_ID,
    GGML_TEMPERATURE,
    GGML_TOP_P,
    logging,
)
from pygptprompt.api.llama import LlamaAPI


@click.command()
@click.option(
    "--repo_id",
    type=click.STRING,
    default=GGML_REPO_ID,
    help="The repository to download the model from. Default is TheBloke/orca_mini_7B-GGML.",
)
@click.option(
    "--filename",
    type=click.STRING,
    default=GGML_FILENAME,
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
    help="Enter a chat loop with the model. Default: False",
)
@click.option(
    "--n_ctx",
    type=click.INT,
    default=GGML_N_CTX,
    help="Maximum context size. Default is 512.",
)
@click.option(
    "--n_batch",
    type=click.INT,
    default=GGML_N_BATCH,
    help="Number of batches to use. Default is 512.",
)
@click.option(
    "--n_gpu_layers",
    type=click.INT,
    default=GGML_N_GPU_LAYERS,
    help="Number of GPU layers to use. Default is 0.",
)
@click.option(
    "--low_vram",
    type=click.BOOL,
    default=GGML_LOW_VRAM,
    help="Set to True if GPU device has low VRAM. Default is False.",
)
@click.option(
    "--max_tokens",
    type=click.INT,
    default=GGML_MAX_TOKENS,
    help="The maximum number of tokens to generate. Default is 512.",
)
@click.option(
    "--temperature",
    type=click.FLOAT,
    default=GGML_TEMPERATURE,
    help="The temperature to use for sampling. Default is 0.8.",
)
@click.option(
    "--top_p",
    type=click.FLOAT,
    default=GGML_TOP_P,
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
    llama = LlamaAPI(
        repo_id=repo_id,
        filename=filename,
        n_ctx=n_ctx,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        low_vram=low_vram,
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
            message: ChatCompletionMessage = llama.get_chat_completions(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            messages.append(message)

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
                message: ChatCompletionMessage = llama.get_chat_completions(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
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
