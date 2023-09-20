"""
pygptprompt/download.py
"""
import logging
import os
import sys

import click
from huggingface_hub import hf_hub_download, model_info
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

logging_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO)


def download_files(repo_id, local_dir, file_names):
    os.makedirs(local_dir, exist_ok=True)
    for file_name in file_names:
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=file_name,
            local_dir=local_dir,
            resume_download=True,
        )
        logging.info(f"Downloaded {file_name} to {model_path}")


def download_model(repo_id, local_dir) -> str:
    logging.info(f"Using {repo_id} to download model data.")
    retries = 0
    max_retries = 3

    try:
        metadata = model_info(repo_id)
        file_names = [x.rfilename for x in metadata.siblings]
        download_files(repo_id, local_dir, file_names)
    except (EntryNotFoundError, RepositoryNotFoundError) as e:
        logging.error(f"Error downloading model: {e}")
        sys.exit(1)
    except LocalEntryNotFoundError as e:
        logging.error(f"Error accessing model: {e}")
        while retries < max_retries and HfApi().is_online():
            logging.info("Retrying download...")
            retries += 1
            download_files(repo_id, local_dir, file_names)
    except Exception as e:
        logging.error(f"Error downloading model: {e}")
        sys.exit(1)


@click.command()
@click.option("--repo_id", help="The Hugging Face repository ID.")
@click.option(
    "--local_dir", help="The directory where you want to store the downloaded files."
)
def main(repo_id, local_dir):
    download_model(repo_id, local_dir)


if __name__ == "__main__":
    main()
