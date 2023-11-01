"""
pygptprompt/cli/upload.py

Docs:
    # NOTE: Manual model uploading is limited and error prone.
    - https://huggingface.co/docs/hub/models-uploading
    # NOTE: Automated uploading is recommended for larger models.
    - https://huggingface.co/docs/huggingface_hub/guides/upload
    - https://huggingface.co/docs/huggingface_hub/v0.17.1/en/package_reference/login#huggingface_hub.login

User Access Token:
    - https://huggingface.co/settings/tokens

NOTE: This is still a Work in Progress.
"""
import sys
from pathlib import Path
from typing import Optional, Union

import click
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt import logging
from pygptprompt.config.manager import ConfigurationManager


def upload_file(
    api: HfApi,
    repo_id: str,
    local_file: Union[str, Path],
    repo_path: str,
    token: Optional[str] = None,
    repo_type: Optional[str] = None,
):
    """
    Upload a file to a specific Hugging Face repository.
    """
    try:
        api.upload_file(
            path_or_fileobj=local_file,
            path_in_repo=repo_path,
            repo_id=repo_id,
            token=token,
            repo_type=repo_type,
        )
        logging.info(f"Successfully uploaded {local_file} to {repo_id}")
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        sys.exit(1)


def upload_folder(
    api,
    repo_id: str,
    local_dir: Union[str, Path],
    token: Optional[str] = None,
    repo_type: Optional[str] = None,
) -> None:
    """
    Upload all files from a local directory to a specific Hugging Face repository.
    """
    try:
        api.upload_folder(
            repo_id=repo_id,
            folder_path=local_dir,
            token=token,
            repo_type=repo_type,
        )
        logging.info(f"Successfully uploaded folder {local_dir} to {repo_id}")
    except Exception as e:
        logging.error(f"Error uploading folder: {e}")


@click.command()
@click.option("-c", "--config_path", help="The configuration file path.")
@click.option("-r", "--repo_id", help="The Hugging Face repository ID.")
@click.option(
    "-t",
    "--repo_type",
    help="The type of repository. `model`, `dataset`, or `space`. defaults to `None`.",
)
@click.option(
    "-p",
    "--path",
    help="The path where you want to read the uploaded files or directories from.",
)
def main(repo_id, repo_type, path, config_path):
    config = None

    if config_path:
        config = ConfigurationManager(config_path)
        token = config.get_environment("HUGGINGFACE_TOKEN")

    api = HfApi()
    api.create_repo(repo_id, exist_ok=True, repo_type=repo_type)

    path_obj = Path(path)
    if path_obj.is_file():
        upload_file(
            api,
            repo_id,
            str(path_obj),
            repo_path=str(path_obj.name),
            token=token,
            repo_type=repo_type,
        )
    elif path_obj.is_dir():
        upload_folder(
            api,
            repo_id,
            str(path_obj),
            token=token,
            repo_type=repo_type,
        )
    else:
        logging.error("The specified path is neither a file nor a directory.")
        sys.exit(1)
