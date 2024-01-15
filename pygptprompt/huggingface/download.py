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
import sys
from logging import Logger
from pathlib import Path
from typing import List, Optional, Union

from huggingface_hub import (
    HfApi,
    dataset_info,
    hf_hub_download,
    login,
    model_info,
    space_info,
)
from huggingface_hub.utils import (
    EntryNotFoundError,
    LocalEntryNotFoundError,
    RepositoryNotFoundError,
)


class HuggingFaceDownload:
    def __init__(
        self,
        token: Optional[str] = None,
        logger: Optional[Logger] = None,
    ):
        """
        Initializes the HuggingFaceDownload object.

        Args:
            token (str, optional): The Hugging Face API token for remote authentication.
            logger (Logger, optional): A custom logger instance for logging, if provided.

        Notes:
            - The implementation details regarding remote authentication are confusing.
            - Hugging Face "supports" multiple options for remote authentication, but
              the actual functionality is unclear.
            - Despite the `token` argument, HfApi's constructor is not respected for
              authentication, leading to potential errors.
            - There were multiple attempts to authenticate, and it's unclear which one
              will function as expected.
            - The documentation and implementation details seem to contradict each other,
              causing frustration and confusion.
        """
        # Authenticate with the Hugging Face API using the provided token
        login(token)

        # Initialize the Hugging Face API client
        self.api = HfApi()

        # Store the token for reference in download_file method
        self.token = token

        # Initialize the logger
        if logger:
            self._logger = logger
        else:
            # If no logger is provided, use a default logger with INFO level
            self._logger = logging.getLogger(self.__class__.__name__)
            self._logger.setLevel(logging.INFO)

    def download_file(
        self,
        local_file: str,
        local_path: str,
        repo_id: str,
        repo_type: Optional[str] = None,
        resume_download: bool = False,
    ) -> str:
        model_path = hf_hub_download(
            repo_id=repo_id,
            repo_type=repo_type,
            filename=local_file,
            local_dir=local_path,
            local_dir_use_symlinks=False,
            force_download=False,
            resume_download=resume_download,
            token=self.token,  # This should work, but doesn't because the argument isn't respected!
        )
        self._logger.info(f"Downloaded {local_file} to {model_path}")
        return model_path

    def _download_all_files(
        self,
        repo_id: str,
        local_path: str,
        local_files: List[str],
        repo_type: Optional[str] = None,
        resume_download: bool = False,
    ) -> List[str]:
        model_paths = []
        for local_file in local_files:
            model_path = self.download_file(
                local_file=local_file,
                local_path=local_path,
                repo_id=repo_id,
                repo_type=repo_type,
                resume_download=resume_download,
            )
            model_paths.append(model_path)
        return model_paths

    def download_folder(
        self,
        local_path: str,
        repo_id: str,
        repo_type: Optional[str] = None,
        resume_download: bool = False,
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
            self._download_all_files(
                repo_id,
                local_path,
                local_files,
                repo_type,
                resume_download,
            )
        except (EntryNotFoundError, RepositoryNotFoundError) as e:
            self._logger.error(f"Error downloading source: {e}")
            sys.exit(1)
        except LocalEntryNotFoundError as e:
            self._logger.error(f"Error accessing source: {e}")
            while retries < max_retries and self.api.is_online():
                self._logger.info("Retrying download...")
                retries += 1
                self._download_all_files(
                    repo_id,
                    local_path,
                    local_files,
                    repo_type,
                    resume_download,
                )
        except Exception as e:
            self._logger.error(f"Error downloading source: {e}")
            sys.exit(1)

    def download(
        self,
        path: Union[str, Path],
        repo_id: str,
        repo_type: Optional[str] = None,
        resume_download: bool = False,
        is_file: bool = False,
    ):
        """
        Download files or directories from a Hugging Face repository.
        """
        # Convert path to a Path object for consistency
        path_obj = Path(path) if isinstance(path, str) else path

        # Create the parent directory if it doesn't exist
        self._logger.info(
            f"Downloading to {'file' if is_file else 'directory'}: {path_obj}"
        )

        if is_file:
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            file_name = path_obj.name
            local_path = path_obj.parent
            self.download_file(
                local_file=file_name,
                local_path=str(local_path),
                repo_id=repo_id,
                repo_type=repo_type,
                resume_download=resume_download,
            )
        else:
            path_obj.mkdir(parents=True, exist_ok=True)
            self.download_folder(
                local_path=str(path_obj),
                repo_id=repo_id,
                repo_type=repo_type,
                resume_download=resume_download,
            )
