"""
pygptprompt/cli/download.py
"""
import click

from pygptprompt.config.manager import ConfigurationManager
from pygptprompt.huggingface.download import HuggingFaceDownload


@click.command()
@click.option("-c", "--config_path", help="The configuration file path.")
@click.option("-r", "--repo_id", help="The Hugging Face repository ID.")
@click.option(
    "-t",
    "--repo_type",
    help="The type of repository. `model`, `dataset`, or `space`. defaults to `None`.",
)
@click.option(
    "-d",
    "--local_dir",
    help="The directory where you want to store the downloaded files.",
)
def main(repo_id, repo_type, local_dir, config_path):
    config = None

    if config_path:
        config = ConfigurationManager(config_path)

    download = HuggingFaceDownload(config)
    download.download_repository(repo_id, local_dir, repo_type)


if __name__ == "__main__":
    main()
