"""
pygptprompt/huggingface/upload.py

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
import logging
import sys
from logging import Logger
from pathlib import Path
from typing import Optional, Union

from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt.pattern.logger import get_default_logger


class HuggingFaceUpload:
    def __init__(
        self,
        token: Optional[str] = None,
        logger: Optional[Logger] = None,
    ):
        self.api = HfApi()
        self.token = token

        if logger:
            self._logger = logger
        else:
            self._logger = get_default_logger(self.__class__.__name__, logging.INFO)

    def upload_file(
        self,
        local_file: Union[str, Path],
        repo_path: str,
        repo_id: str,
        repo_type: Optional[str] = None,
    ):
        try:
            self.api.upload_file(
                path_or_fileobj=local_file,
                path_in_repo=repo_path,
                repo_id=repo_id,
                token=self.token,
                repo_type=repo_type,
            )
            self._logger.info(f"Successfully uploaded {local_file} to {repo_id}")
        except Exception as e:
            self._logger.error(f"Error uploading file: {e}")
            sys.exit(1)

    def upload_folder(
        self,
        local_path: Union[str, Path],
        repo_id: str,
        repo_type: Optional[str] = None,
    ):
        try:
            self.api.upload_folder(
                repo_id=repo_id,
                folder_path=local_path,
                token=self.token,
                repo_type=repo_type,
            )
            self._logger.info(f"Successfully uploaded folder {local_path} to {repo_id}")
        except Exception as e:
            self._logger.error(f"Error uploading folder: {e}")
            sys.exit(1)

    def _create_repository(self, repo_id: str, repo_type: str):
        try:
            self.api.create_repo(
                repo_id,
                token=self.token,
                exist_ok=True,
                repo_type=repo_type,
            )
            self._logger.info(f"Successfully created {repo_type} for {repo_id}")
        except Exception as e:
            self._logger.error(f"Error uploading folder: {e}")
            sys.exit(1)

    def upload(
        self,
        path: Union[str, Path],
        repo_id: str,
        repo_type: Optional[str] = None,
    ):
        path_obj = Path(path)

        # NOTE: Create the repository if it doesn't exist.
        self._create_repository(repo_id, repo_type)

        if path_obj.is_file():
            self.upload_file(
                local_file=str(path_obj),
                repo_path=str(path_obj.name),
                repo_id=repo_id,
                repo_type=repo_type,
            )
        elif path_obj.is_dir():
            self.upload_folder(
                local_path=str(path_obj),
                repo_id=repo_id,
                repo_type=repo_type,
            )
        else:
            self._logger.error("The specified path is neither a file nor a directory.")
            sys.exit(1)
