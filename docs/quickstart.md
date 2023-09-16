# Quickstart Guide

## Starting the Chat Interface

To get started with the chat interface, execute the following command:

```sh
python -m pygptprompt.chat --chat [SESSION_NAME] [CONFIG_PATH]
```

This command initializes a chat session using the specified session name and
configuration file path. If you omit either, the system will resort to defaults
or prompts.

### Note:

As of this pre-release, IRC-like commands are temporarily disabled. However, GPT
model function calling is fully supported.

## Available Commands and Options

Within the chat interface, you can call GPT model functions for various tasks.
Although IRC-like commands are disabled, you can still interact robustly with
the model.

To specify a different configuration file located outside of the current working
directory, use the `--config` option:

```sh
python -m pygptprompt.chat --config /path/to/config.json
```

## Additional Command Line Options

These command-line options offer a customized experience:

- `--prompt TEXT`: Initial model prompt.
- `--embed`: Utilize the chroma vector database.
- `--provider TEXT`: Choose the model provider ('openai' for GPT models and
  'llama_cpp' for Llama models).
- `--path_database TEXT`: Specify the path for storing embeddings.

Run `python -m pygptprompt.chat --help` to see all available options.

## Keybindings

The following default keybindings facilitate interaction:

- `Ctrl-C`, `Ctrl-D`: Exit the application.
- `Return`: Insert a newline.
- `Alt-Return` (Win & Linux) / `Option-Return` (Mac OS X): Submit a message.
- `Up/Down arrow keys`: Navigate command history.
- `Ctrl-Shift-V`: Paste from clipboard.
- `Tab`: Auto-complete for commands and arguments is in development.

## Example Session

Here's an example session for your reference:

```sh
(.venv) git:(main | Δ) λ python -m pygptprompt.chat --chat dev tests/config.dev.json
system
Your name is GPT. You are a pair programming assistant. For further information, use model function calls...
```
