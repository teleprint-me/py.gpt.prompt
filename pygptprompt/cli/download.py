"""
pygptprompt/cli/download.py
"""
import logging
import os
import sys

import click
from huggingface_hub import hf_hub_download, login, model_info
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.logger import get_default_logger

logger = get_default_logger("Download", logging.INFO)


def download_files(repo_id, local_dir, file_names) -> None:
    os.makedirs(local_dir, exist_ok=True)
    for file_name in file_names:
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=file_name,
            local_dir=local_dir,
            resume_download=True,
            local_dir_use_symlinks=False,
        )
        logger.info(f"Downloaded {file_name} to {model_path}")


def download_model(repo_id, local_dir) -> None:
    logger.info(f"Using {repo_id} to download model data.")
    retries = 0
    max_retries = 3

    try:
        metadata = model_info(repo_id)
        file_names = [x.rfilename for x in metadata.siblings]
        download_files(repo_id, local_dir, file_names)
    except (EntryNotFoundError, RepositoryNotFoundError) as e:
        logger.error(f"Error downloading model: {e}")
        sys.exit(1)
    except LocalEntryNotFoundError as e:
        logger.error(f"Error accessing model: {e}")
        while retries < max_retries and HfApi().is_online():
            logger.info("Retrying download...")
            retries += 1
            download_files(repo_id, local_dir, file_names)
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        sys.exit(1)


@click.command()
@click.option("-c", "--config_path", help="The configuration file path.")
@click.option("-r", "--repo_id", help="The Hugging Face repository ID.")
@click.option(
    "-d",
    "--local_dir",
    help="The directory where you want to store the downloaded files.",
)
def main(repo_id, local_dir, config_path):
    if config_path:
        config = ConfigurationManager(config_path, logger=logger)
        token = config.get_environment("HUGGINGFACE_TOKEN")
        login(token)

    download_model(repo_id, local_dir)


if __name__ == "__main__":
    main()
