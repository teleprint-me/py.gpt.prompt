"""
pygptprompt/huggingface_hub/download.py

Docs:
    # NOTE: Manual model downloading is limited and error prone.
    - https://huggingface.co/docs/hub/models-downloading
    # NOTE: Automated downloading is recommended for larger models.
    - https://huggingface.co/docs/huggingface_hub/main/en/package_reference/file_download

User Access Token:
    - https://huggingface.co/settings/tokens

NOTE: This is still a Work in Progress.
"""
import logging
import os
import sys
from logging import Logger
from pathlib import Path
from typing import List, Optional, Union

from huggingface_hub import dataset_info, hf_hub_download, model_info, space_info
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt.pattern.logger import get_default_logger


class HuggingFaceDownload:
    def __init__(
        self,
        token: Optional[str] = None,
        logger: Optional[Logger] = None,
    ):
        self.api = HfApi()
        self.token = None

        if logger:
            self._logger = logger
        else:
            self._logger = get_default_logger(self.__class__.__name__, logging.INFO)

    def download_file(
        self,
        local_file: str,
        local_path: str,
        repo_id: str,
        repo_type: Optional[str] = None,
    ) -> str:
        model_path = hf_hub_download(
            repo_id=repo_id,
            repo_type=repo_type,
            filename=local_file,
            local_dir=local_path,
            local_dir_use_symlinks=False,
            resume_download=True,
            token=self.token,
        )
        self._logger.info(f"Downloaded {local_file} to {model_path}")
        return model_path

    def _download_all_files(
        self,
        repo_id: str,
        local_path: str,
        local_files: List[str],
        repo_type: Optional[str] = None,
    ) -> List[str]:
        model_paths = []
        os.makedirs(local_path, exist_ok=True)
        for local_file in local_files:
            model_path = self.download_file(
                local_file=local_file,
                local_path=local_path,
                repo_id=repo_id,
                repo_type=repo_type,
            )
            model_paths.append(model_path)
        return model_paths

    def download_folder(
        self,
        local_path: str,
        repo_id: str,
        repo_type: Optional[str] = None,
    ) -> None:
        # NOTE: Consider resetting `retries` to zero if a retry is successful.
        self._logger.info(f"Using {repo_id} to download source data.")
        retries = 0
        max_retries = 3

        try:
            if repo_type == "dataset":
                metadata = dataset_info(repo_id)
            elif repo_type == "space":
                metadata = space_info(repo_id)
            else:
                metadata = model_info(repo_id)

            local_files = [x.rfilename for x in metadata.siblings]
            self._download_all_files(repo_id, local_path, local_files, repo_type)
        except (EntryNotFoundError, RepositoryNotFoundError) as e:
            self._logger.error(f"Error downloading source: {e}")
            sys.exit(1)
        except LocalEntryNotFoundError as e:
            self._logger.error(f"Error accessing source: {e}")
            while retries < max_retries and self.api.is_online():
                self._logger.info("Retrying download...")
                retries += 1
                self._download_all_files(repo_id, local_path, local_files, repo_type)
        except Exception as e:
            self._logger.error(f"Error downloading source: {e}")
            sys.exit(1)

    def download(
        self,
        path: Union[str, Path],
        repo_id: str,
        repo_type: Optional[str] = None,
    ):
        path_obj = Path(path)

        if path_obj.is_file():
            file_name = path_obj.name
            local_path = path_obj.parent
            self.download_file(
                local_file=file_name,
                local_path=str(local_path),
                repo_id=repo_id,
                repo_type=repo_type,
            )
        elif path_obj.is_dir():
            self.download_folder(
                local_path=str(path_obj),
                repo_id=repo_id,
                repo_type=repo_type,
            )
        else:
            self._logger.error("The specified path is neither a file nor a directory.")
            sys.exit(1)
