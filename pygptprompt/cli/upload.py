"""
pygptprompt/cli/upload.py

NOTE: This is still a Work in Progress.
"""
import click

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.huggingface.upload import HuggingFaceUpload


@click.command()
@click.option(
    "-c",
    "--config_path",
    help="The configuration file path. Overrides settings if specified.",
)
@click.option(
    "-r",
    "--repo_id",
    prompt="Hugging Face repository ID",
    help="The Hugging Face repository ID.",
)
@click.option(
    "-t",
    "--repo_type",
    help="The type of repository. `model`, `dataset`, or `space`. Defaults to `None`.",
)
@click.option(
    "-p",
    "--local_path",
    prompt="Local path to upload",
    help="The local path from which to upload files or directories.",
)
@click.option(
    "-a",
    "--api_token",
    help="Hugging Face API token. Overrides configuration file.",
)
def main(repo_id, repo_type, local_path, config_path, api_token):
    if not api_token and config_path:
        config = ConfigurationManager(config_path)
        api_token = config.get_environment("HUGGINGFACE_TOKEN")

    upload = HuggingFaceUpload(api_token)
    upload.upload(local_path, repo_id, repo_type)
