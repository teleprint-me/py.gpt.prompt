"""
pygptprompt/cli/huggingface_hub.py

NOTE: This is still a Work in Progress.
"""

import click

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.huggingface.hub.download import HuggingFaceDownload
from pygptprompt.huggingface.hub.upload import HuggingFaceUpload


def common_options(command_func):
    decorators = [
        click.option(
            "-r",
            "--repo_id",
            prompt="Hugging Face repository ID",
            help="The Hugging Face repository ID.",
        ),
        click.option(
            "-t",
            "--repo_type",
            help="The type of repository. `model`, `dataset`, or `space`. Defaults to `None`.",
        ),
        click.option(
            "-c",
            "--config_path",
            help="The configuration file path.",
        ),
        click.option(
            "-a",
            "--api_token",
            help="Hugging Face API token. Overrides configuration file.",
        ),
    ]
    for decorator in reversed(decorators):
        command_func = decorator(command_func)
    return command_func


@click.group()
def cli():
    pass


@cli.command(name="upload")
@click.option(
    "-p",
    "--local_path",
    prompt="Local path to upload",
    help="The local path from which to upload files or directories.",
)
@common_options
def upload_command(repo_id, repo_type, local_path, config_path, api_token):
    if not api_token and config_path:
        config = ConfigurationManager(config_path)
        api_token = config.get_environment("HUGGINGFACE_WRITE_API")

    huggingface = HuggingFaceUpload(api_token)
    huggingface.upload(local_path, repo_id, repo_type)


@cli.command(name="download")
@click.option(
    "-p",
    "--local_path",
    prompt="Local path to download",
    help="The local path from which to download files or directories.",
)
@click.option(
    "-f",
    "--file",
    is_flag=True,
    help="Specify this flag if the local path is a file. If not set, the path is treated as a directory.",
)
@click.option(
    "-d",
    "--resume",
    is_flag=True,
    help="Specify this flag to continue downloading partially downloaded files. If not set, the download will start over.",
)
@common_options
def download_command(
    repo_id,
    repo_type,
    local_path,
    resume,
    file,
    config_path,
    api_token,
):
    if not api_token and config_path:
        config = ConfigurationManager(config_path)
        api_token = config.get_environment("HUGGINGFACE_READ_API")

    huggingface = HuggingFaceDownload(api_token)
    huggingface.download(local_path, repo_id, repo_type, resume, file)


if __name__ == "__main__":
    cli()
