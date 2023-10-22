# Downloading Models from Hugging Face

PyGPTPrompt provides a convenient command-line interface (CLI) tool for
downloading models from the Hugging Face model hub. This tool allows you to
access and utilize a wide range of pre-trained models for various natural
language processing (NLP) tasks. You can easily specify the model you want to
download and the directory where you want to store the downloaded files.

## Prerequisites

Before using the `pygptprompt.cli.download` tool, make sure you have the
following prerequisites:

1. **PyGPTPrompt Installation**: Ensure that you have PyGPTPrompt installed on
   your system. You can follow the installation instructions provided in the
   [PyGPTPrompt documentation](https://github.com/teleprint-me/py.gpt.prompt/tree/main/docs/install)
   to set up the environment.

2. **Hugging Face Token (Optional)**: If you intend to access gated models on
   the Hugging Face model hub that require authentication, you must provide an
   Hugging Face API token. This token should be placed in a `.env` file, and the
   tool will look for it when accessing the model hub. The path to the `.env`
   file is sourced from the configuration file, and the configuration file is
   specified using the `--config_path` option.

Example of a `config.json` referencing the `.env` file:

```json
{
  "app": {
    "provider": "pygptprompt",
    "local": {
      "path": "${HOME}/.local/pygptprompt/",
      "type": "dir"
    },
    "env": {
      "path": "${HOME}/.local/pygptprompt/.env",
      "type": "file"
    },
    // other paths and rules...
  // other configuration settings...
}
```

The `.env` file should contain your Hugging Face API token:

```dotenv
HUGGINGFACE_TOKEN=your-api-token-here
```

This separation of concerns protects developers from exposing sensitive data
during development because the configurations are committed and shared publicly.

## Usage

To download models from Hugging Face using the `pygptprompt.cli.download` tool,
follow these steps:

```sh
python -m pygptprompt.cli.download [OPTIONS]
```

### Options

- `-c, --config_path TEXT`: Specifies the path to the configuration file. This
  file may reference a path to a `.env` file containing the Hugging Face API
  token, allowing access to gated models. If not provided, the tool will attempt
  to download models without authentication.

- `-r, --repo_id TEXT`: The Hugging Face repository ID of the model you want to
  download. You can find the repository ID on the Hugging Face model hub. This
  option is required.

- `-d, --local_dir TEXT`: Specifies the directory where you want to store the
  downloaded model files. The downloaded files will be organized within this
  directory. This option is required.

### Example

Here's an example of how to use the `pygptprompt.cli.download` tool to download
a model:

```sh
python -m pygptprompt.cli.download -r username/model-name -d /path/to/downloaded/models
```

In this example, replace `username/model-name` with the repository ID of the
model you want to download, and `/path/to/downloaded/models` with the desired
directory for storing the downloaded files.

## Important Notes

- The `pygptprompt.cli.download` tool provides access to models hosted on the
  Hugging Face model hub. You can explore and find various pre-trained models
  for different NLP tasks on the Hugging Face website.

- If you have an Hugging Face API token and wish to access gated models, ensure
  that the token is placed in the `.env` file as described above.

---

Please review this revised content, and let me know if any further adjustments
or additions are needed.
