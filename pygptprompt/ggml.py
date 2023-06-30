import os

import click
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from pygptprompt import logging


@click.command()
@click.option(
    "--repo_id",
    type=click.STRING,
    default="TheBloke/orca_mini_7B-GGML",
)
@click.option(
    "--filename",
    type=click.STRING,
    default="orca-mini-7b.ggmlv3.q4_0.bin",
)
@click.option(
    "--text_input",
    type=click.STRING,
    default="",
)
@click.option(
    "--low_vram",
    type=click.BOOL,
    default=False,
)
def main(repo_id, filename, text_input, low_vram):
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")

    logging.info(f"Using {repo_id} to load {filename}")

    if not os.path.exists(cache_dir):
        logging.info(
            f"Model not found locally. Downloading {filename} from Hugging Face Hub using {repo_id}."
        )
    else:
        logging.info(f"Model found locally. Loading {filename} from cache instead.")

    model_path = hf_hub_download(
        repo_id=repo_id, filename=filename, cache_dir=cache_dir
    )

    logging.info(f"Using {model_path} to load {repo_id} into memory")

    if not text_input:
        text_input = input("> ")
    system_prompt = (
        "### System:\n"
        "My name is Orca. I am an AI assistant that follows instruction extremely well. I am a very helpful assistant.\n\n"
    )
    user_prompt = f"### User:\n{text_input}\n\n"

    model_prompt = "### Response:"

    prompt = system_prompt + user_prompt + model_prompt
    llm = Llama(
        model_path=model_path,
        n_gpu_layers=10,
        n_batch=64,
        low_vram=low_vram,
    )
    output = llm(prompt, max_tokens=32, stop=["### User:\n", "\n"], echo=True)
    print(output)


if __name__ == "__main__":
    main()
