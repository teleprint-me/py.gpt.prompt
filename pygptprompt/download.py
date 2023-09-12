"""
pygptprompt/download.py
"""

import sys

import click
from huggingface_hub import hf_hub_download, model_info
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt import logging


def download_model(repo_id, local_dir) -> str:
    """
    Download the model file to a custom directory path.

    Returns:
        str: The path to the downloaded model file.
    """
    logging.info(f"Using {repo_id} to download model data.")
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            metadata = model_info(repo_id)
            file_names = [x.rfilename for x in metadata.siblings]

            for file_name in file_names:
                model_path = hf_hub_download(
                    repo_id=repo_id,
                    filename=file_name,
                    local_dir=local_dir,
                    resume_download=True,
                )
                logging.info(f"Downloaded {file_name} to {model_path}")

        except (EntryNotFoundError, RepositoryNotFoundError) as e:
            logging.error(f"Error downloading {file_name}: {e}")
            logging.error(f"Error downloading model: {e}")
            sys.exit(1)
        except LocalEntryNotFoundError as e:
            logging.error(f"Error accessing model: {e}")
            if HfApi().is_online():
                logging.info("Retrying download...")
                retries += 1
            else:
                logging.error("Network is not available. Cannot retry download.")
                sys.exit(1)
        except Exception as e:
            logging.error(f"Error downloading model: {e}")
            sys.exit(1)

    logging.error("Max retries exceeded. Failed to download the model.")
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
