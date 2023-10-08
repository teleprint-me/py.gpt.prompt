"""
pygptprompt/cli/upload.py

Docs:
    # NOTE: Manual model uploading is limited and error prone.
    - https://huggingface.co/docs/hub/models-uploading
    # NOTE: Automated model uploading is recommended for larger models.
    - https://huggingface.co/docs/huggingface_hub/guides/upload
    - https://huggingface.co/docs/huggingface_hub/v0.17.1/en/package_reference/login#huggingface_hub.login

User Access Token:
    - https://huggingface.co/settings/tokens

NOTE: This is still a Work in Progress and is mostly a copy and past of the download script. Modifications are still required in order for it to operate as expected.
"""
import sys

import click
from huggingface_hub import login, logout, model_info
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt import logging


def upload_file():
    # Once you’ve created a repository with create_repo(),
    # you can upload a file to your repository using upload_file().
    # api = HfApi()
    # api.create_repo
    # api.upload_file(
    #     path_or_fileobj="/path/to/local/folder/README.md",
    #     path_in_repo="README.md",
    #     repo_id="username/test-dataset",
    #     repo_type="dataset",
    # )
    ...


def upload_folder(repo_id, local_dir, file_names):
    # api = HfApi()
    # Upload all the content from the local folder to your remote Space.
    # By default, files are uploaded at the root of the repo
    # api.upload_folder(
    #     folder_path="/path/to/local/space",
    #     repo_id="username/my-cool-space",
    #     repo_type="space",
    # )
    ...


def upload_model(repo_id, local_dir) -> str:
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
    upload_model(repo_id, local_dir)


if __name__ == "__main__":
    main()
