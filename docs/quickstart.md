# Quickstart Guide

## PyGPTPrompt: Prototype Phase

This project is currently in its prototype phase. Some features are still under
development or may be temporarily disabled. Your patience and feedback are
highly appreciated.

## Launching the Chat Interface

To initiate a chat session, run the following command:

```sh
python -m pygptprompt.chat [SESSION_NAME] [CONFIG_PATH]
```

This command will initialize a chat session, taking into account the session
name and configuration file path you provide. If omitted, defaults or prompts
will apply.

### Important:

In this pre-release, IRC-like commands are not available. Nevertheless, GPT
model function calling is fully enabled.

## Commands and Options

The chat interface supports various GPT model functions. Although IRC-like
commands are currently unavailable, robust interactions are still possible,
including the ability to recall past information.

### Basic Usage

To specify both the session name and configuration file path, enter them as
arguments:

```sh
python -m pygptprompt.chat your_session_name /your/config/path.json
```

### Advanced Features

#### Enhanced Memory Capabilities

Use the `--embed` flag to activate GPT model memory features:

```sh
python -m pygptprompt.chat [SESSION_NAME] [CONFIG_PATH] --embed
```

## Additional CLI Options

Customize your experience with these additional command-line options:

- `--prompt TEXT`: Set an initial prompt.
- `--embed`: Activate chroma vector database.
- `--provider TEXT`: Choose between 'openai' and 'llama_cpp' as the model
  provider.
- `--path_database TEXT`: Define the path for embedding storage.

For a complete list, run:

```sh
python -m pygptprompt.chat --help
```

## Key Shortcuts

Here are default key shortcuts for easier interaction:

- `Ctrl-C`, `Ctrl-D`: Exit the app.
- `Return`: Add a new line.
- `Alt-Return` (Win & Linux) / `Option-Return` (Mac): Submit a message.
- `Up/Down Arrows`: Navigate command history.
- `Ctrl-Shift-V`: Paste content.
- `Tab`: Command and argument auto-complete (under development).

## Example Interaction

Here's a quick example to guide you through:

```sh
(.venv) git:(main | Δ) λ python -m pygptprompt.chat your_session_name /your/config/path.json
system
My name is ChatGPT. I am a helpful assistant. I will only use the functions I have been provided with.
```

## Additional Tools and Functionalities

PyGPTPrompt comes packed with a variety of specialized tools and
functionalities, each residing in its own dedicated module or package:

### Modules

- `chat.py`: The primary interface for interactive chat sessions.
- `convert.py`: Converts compatible Hugging Face models to GGUF (Georgi Gerganov
  Unified Format) for `llama.cpp` support.
- `download.py`: A utility for manually downloading selected models from Hugging
  Face.
- `embed.py`: Manages vector-based embeddings in the vector database for model
  memory recall.
- `llama.py`: An example script from Facebook Research Labs, intended for future
  integration to support non-quantized, full-sized models.
- `ocr.py`: Converts images to text via Optical Character Recognition.
- `pdf.py`: Transforms PDFs into textual data.
- `quantize.py`: Provides quantization for converting HF models to GGUF format.

### Packages

- `function`: Enables custom function calls for GPT models. (Support for Llama
  models is under development.)
- `model`: A factory module for managing different types of models.

**Future Developments**:

- Uploading and fine-tuning features (`upload.py` and `finetune.py`) are in the
  roadmap and will be added in upcoming releases. They are currently represented
  as uncommitted stub files.

Feel free to explore these modules to maximize the utility you derive from
PyGPTPrompt.
