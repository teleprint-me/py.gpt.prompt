# Interacting with Hugging Face Hub

PyGPTPrompt offers a comprehensive command-line interface (CLI) for both
downloading and uploading models, datasets, and spaces to and from the Hugging
Face Hub. This enhancement allows for greater flexibility in leveraging a wide
array of pre-trained assets.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [Subcommands](#subcommands)
- [Options: What's Required and When](#options-whats-required-and-when)
- [Important Notes](#important-notes)

## Prerequisites

The prerequisites remain largely unchanged:

1. **PyGPTPrompt Installation**: Follow the installation instructions in the
   [PyGPTPrompt documentation](install/user.md).

2. **Hugging Face Tokens for Reading and Writing**:

   - **Reading (Conditional)**: The `HUGGINGFACE_READ_API` key is optional for
     most public models, datasets, or spaces but offers rate-limiting benefits.
     It becomes mandatory if you're accessing gated content. Store the token in
     a `.env` file sourced from `config.json` if required.

   - **Writing (Required)**: To upload models, datasets, or spaces, you will
     need to use the `HUGGINGFACE_WRITE_API` key for authentication. This is
     always required for write operations.

Place your Hugging Face API tokens in a `.env` file:

```dotenv
HUGGINGFACE_READ_API=your-read-api-token-here (Optional for public content, Required for gated content)
HUGGINGFACE_WRITE_API=your-write-api-token-here (Required)
```

## Usage

The CLI tool has been restructured to include subcommands for downloading and
uploading:

```sh
python -m pygptprompt.cli.huggingface_hub [OPTIONS] COMMAND [ARGS]...
```

### Subcommands

1. **download**: Downloads models or datasets from the Hugging Face Hub.
2. **upload**: Uploads models or datasets to the Hugging Face Hub.

#### Download Example

```sh
python -m pygptprompt.cli.huggingface_hub download -r smallcloudai/Refact-1_6B-fim -p models/smallcloudai/Refact-1_6B-fim
```

#### Upload Example

```sh
python -m pygptprompt.cli.huggingface_hub upload -c tests/config.dev.json -r teleprint-me/refact-1.6B-fim-gguf -p models/smallcloudai/Refact-1_6B-fim/refact-1.6B-fim-q8_0.gguf
```

## Options: What's Required and When

Common options for both `download` and `upload`:

- `-p, --local_path TEXT`: The local path for download or upload.
- `-r, --repo_id TEXT`: The Hugging Face repository ID.
- `-t, --repo_type TEXT`: The type of repository: `model`, `dataset`, or
  `space`. Defaults to `model`.
- `-c, --config_path TEXT`: The path to the configuration file.
- `-a, --api_token TEXT`: Overrides the API token specified in the configuration
  file.

### What's Required and When

- `repo_id` and `local_path` are the only required options in most cases.
- Using the `repo_type` option will be required when interacting with a
  `dataset` or `space`. Otherwise, it defaults to `model`.
- The `api_token` option can be used to bypass setting up an `.env` file if you
  still need to authenticate with the Hugging Face Hub API.

## Important Notes

- You can now upload models and datasets in addition to downloading them,
  providing a more holistic interaction with the Hugging Face Hub.
