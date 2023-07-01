import os
import sys
from typing import List

import click
from huggingface_hub import hf_hub_download
from llama_cpp import ChatCompletionMessage, Llama

from pygptprompt import (
    DEFAULT_MODEL_FILENAME,
    DEFAULT_MODEL_REPOSITORY,
    DEFAULT_N_BATCH,
    DEFAULT_N_GPU_LAYERS,
    logging,
)


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
    help="The filename of the model from the given repository. Default is orca-mini-7b.ggmlv3.q4_0.bin.",
)
@click.option(
    "--text_input",
    type=click.STRING,
    default="Hello! What is your name?",
    help="Literal string based text input provided by the user. Default is a greeting.",
)
@click.option(
    "--n_gpu_layers",
    type=click.INT,
    default=DEFAULT_N_GPU_LAYERS,
    help="Number of GPU layers to use. Default is 0.",
)
@click.option(
    "--n_batch",
    type=click.INT,
    default=DEFAULT_N_BATCH,
    help="Number of batches to use. Default is 512.",
)
@click.option(
    "--low_vram",
    type=click.BOOL,
    default=False,
    help="Set to True if GPU device has low VRAM. Default is False.",
)
@click.option(
    "--max_tokens",
    type=click.INT,
    default=512,
    help="The maximum number of tokens to generate. Default is 64.",
)
@click.option(
    "--temperature",
    type=click.FLOAT,
    default=0.8,
    help="The temperature to use for sampling. Default is 0.8.",
)
@click.option(
    "--top_p",
    type=click.FLOAT,
    default=0.95,
    help="The top-p value to use for sampling. Default is 0.95.",
)
@click.option(
    "--echo",
    type=click.BOOL,
    default=False,
    help="Whether to echo the prompt. Default is True.",
)
def main(
    repo_id,
    filename,
    text_input,
    n_gpu_layers,
    n_batch,
    low_vram,
    max_tokens,
    temperature,
    top_p,
    echo,
):
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")

    logging.info(f"Using {repo_id} to load {filename}")

    try:
        if not os.path.exists(cache_dir):
            logging.info(
                f"Model not found locally. Downloading {filename} from Hugging Face Hub using {repo_id}."
            )
        else:
            logging.info(f"Model found locally. Loading {filename} from cache instead.")

        model_path = hf_hub_download(
            repo_id=repo_id, filename=filename, cache_dir=cache_dir
        )
    except Exception as e:
        logging.error(f"Error downloading model: {e}")
        sys.exit(1)

    logging.info(f"Using {model_path} to load {repo_id} into memory")

    if not text_input:
        text_input = input("> ")

    # chat_completion_message = ChatCompletionMessage(
    #     role="system",
    #     content="My name is Orca. I am a helpful AI assistant.",
    # )

    system_prompt = "### System:\nMy name is Orca. I am a helpful AI assistant.\n\n"

    user_prompt = f"### User:\n{text_input}\n\n"

    model_prompt = "### Response:"

    prompt = system_prompt + user_prompt + model_prompt

    try:
        llama_model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch,
            low_vram=low_vram,
            verbose=False,
        )

        logging.info("Generating response...")

        response = llama_model.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=echo,
            stream=True,
        )

        print("assistant:", end="")
        sys.stdout.flush()
        for token in response:
            print(token["choices"][0]["text"], end="")
            sys.stdout.flush()
        print()
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
