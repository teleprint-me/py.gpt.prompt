"""
pygptprompt/huggingface_hub/download.py

TODO: Work in progress.
"""
import logging
import os
import sys
from logging import Logger
from typing import List, Optional

from huggingface_hub import dataset_info, hf_hub_download, model_info, space_info
from huggingface_hub.hf_api import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.pattern.logger import get_default_logger


class HuggingFaceDownload:
    def __init__(
        self,
        config: Optional[ConfigurationManager] = None,
        logger: Optional[Logger] = None,
    ):
        self.token = False

        if config:
            self.token = config.get_environment("HUGGINGFACE_TOKEN")

        if logger:
            self._logger = logger
        else:
            self._logger = get_default_logger(self.__class__.__name__, logging.INFO)

    def download_file(
        self,
        repo_id: str,
        local_dir: str,
        file_name: List[str],
        repo_type: Optional[str] = None,
    ) -> str:
        model_path = hf_hub_download(
            repo_id=repo_id,
            repo_type=repo_type,
            filename=file_name,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            resume_download=True,
            token=self.token,
        )
        self._logger.info(f"Downloaded {file_name} to {model_path}")
        return model_path

    def download_all_files(
        self,
        repo_id: str,
        local_dir: str,
        file_names: List[str],
        repo_type: Optional[str] = None,
    ) -> List[str]:
        model_paths = []
        os.makedirs(local_dir, exist_ok=True)
        for file_name in file_names:
            model_path = self.download_file(
                repo_id=repo_id,
                local_dir=local_dir,
                file_name=file_name,
                repo_type=repo_type,
            )
            model_paths.append(model_path)
        return model_paths

    def download_repository(
        self,
        repo_id: str,
        local_dir: str,
        repo_type: Optional[str] = None,
    ) -> None:
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

            file_names = [x.rfilename for x in metadata.siblings]
            self.download_all_files(repo_id, local_dir, file_names, repo_type)
        except (EntryNotFoundError, RepositoryNotFoundError) as e:
            self._logger.error(f"Error downloading source: {e}")
            sys.exit(1)
        except LocalEntryNotFoundError as e:
            self._logger.error(f"Error accessing source: {e}")
            while retries < max_retries and HfApi().is_online():
                self._logger.info("Retrying download...")
                retries += 1
                self.download_all_files(repo_id, local_dir, file_names, repo_type)
        except Exception as e:
            self._logger.error(f"Error downloading source: {e}")
            sys.exit(1)
