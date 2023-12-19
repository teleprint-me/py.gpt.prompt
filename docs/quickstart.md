# Quickstart Guide for PyGPTPrompt

## PyGPTPrompt: Prototype Phase

This project is currently in its prototype phase, with some features under development or temporarily disabled. I appreciate your patience and any feedback as PyGPTPrompt continues to evolve.

## Launching the Chat Interface

Initiate a chat session with this command:

```sh
python -m pygptprompt.cli.chat [CONFIG_PATH] -s [SESSION_NAME]
```

This initializes a chat session using the specified configuration file and session name. Note that a configuration path and session name are currently required.

### Note on IRC-like Commands

Currently, IRC-like commands are disabled during this refactoring phase. For detailed information on these features, please refer to `docs/features.md`. These commands are designed to streamline interactions, such as fetching web pages, browsing content, or executing a task or command.

## Commands and Options

While IRC-like commands are temporarily unavailable, the chat interface still supports robust interactions with GPT models, including memory recall capabilities.

### Basic Usage

To start a session with both session name and configuration path:

```sh
python -m pygptprompt.cli.chat /your/config/path.json -s your_session_name
```

### Advanced Features

#### Enhanced Memory Capabilities

Activate augmented memory features with the `--memory` flag:

```sh
python -m pygptprompt.cli.chat [CONFIG_PATH] -s [SESSION_NAME] -m
```

## Additional CLI Options

Customize your chat experience:

- `--prompt TEXT`: Sets an initial prompt for the session.
- `--chat`: Activates interactive chat mode.
- `--memory`: Enables the chroma vector database for enhanced recall.
- `--provider TEXT`: Choose the model provider (options: 'openai', 'llama_cpp').

For a full list of options, use:

```sh
python -m pygptprompt.cli.chat --help
```

## Key Shortcuts for Navigation

- `Ctrl-C`, `Ctrl-D`: Exit the application.
- `Return`: Insert a new line.
- `Alt-Return` (Win & Linux) / `Option-Return` (Mac): Send a message.
- `Up/Down Arrows`: Browse through command history.
- `Ctrl-Shift-V`: Paste from clipboard.
- `Tab`: (Future Feature) Will support command and argument auto-complete.

## Example Interaction

Here's a sample interaction to get you started:

```shell
(.venv) git:(main | Δ) λ python -m pygptprompt.cli.chat tests/config.dev.json -s test2 -p openai -m -c
2023-10-21 22:45:28,921 - json.py:110 - DEBUG - JSON successfully loaded from tests/config.dev.json
...
system
My name is ChatGPT. I am a helpful assistant.

user
Hello, my name is Austin. What's your name?

assistant
Hello Austin! My name is ChatGPT. How can I assist you today?
```

## Understanding the Configuration File

For setup details and customization, see `docs/configuration.md`. This document explains the configuration file's role in setting up your chat session.

## Example Interaction

Here's a quick example to guide you through:

```shell
(.venv) git:(main | Δ) λ python -m pygptprompt.cli.chat tests/config.dev.json -s test2 -p openai -m -c
2023-10-21 22:45:28,921 - json.py:110 - DEBUG - JSON successfully loaded from tests/config.dev.json
WARNING:root:Database connection is closed.
INFO:SQLiteMemoryStore:Table memory_test2 already exists.
system
My name is ChatGPT. I am a helpful assistant. I will only use the functions I have been provided with.

user
Hello, my name is Austin. What's your name?

assistant
Hello Austin! My name is ChatGPT. How can I assist you today?
```

## Additional Tools and Functionalities

PyGPTPrompt comes packed with a variety of specialized tools and
functionalities, each residing in its own dedicated module or package. The CLI
tools are now available within the `pygptprompt/cli` package and can be called
using `python -m pygptprompt.cli.<module>`.

### Modules

- **`chat.py`**: Provides an interactive chat interface with models, supporting enhanced conversation flows and memory features.
- **`huggingface_hub.py`**: Facilitates downloading and uploading models, datasets, and spaces from/to the Hugging Face Hub, streamlining interactions with a wide array of AI assets.
- **`embed.py`**: Manages vector-based embeddings, enabling augmented episodic memory for models, enhancing recall and context management (Currently a Work in Progress).
- **`llama.py`**: A module designed for integration with LLaMA models, aiming to support both quantized and non-quantized versions.
- **`ocr.py`**: Utilizes Optical Character Recognition technology to convert images to text, enabling models to process and interact with image-based data.
- **`pdf.py`**: Extracts and transforms textual data from PDF files, making it accessible for natural language processing tasks.
- **`quantize.py`**: Offers quantization tools for GGUF format conversion, optimizing models for use with `llama.cpp`.

### Packages

- **`dump`**: Includes tools like `torch.py` and `gguf` for inspecting various model formats, enabling conversion for unsupported models or deeper inspection for debugging purposes.
- **`convert`**: Includes tools like `torch_to_gguf.py` for converting various model formats to GGUF, enabling compatibility with `llama.cpp`.
- **`function`**: Facilitates the implementation of custom function calls within GPT models, enhancing interactivity and functionality. Expansion to support LLaMA models is underway.
- **`model`**: Acts as a model factory, simplifying the management and utilization of various AI models across different providers and formats.

### Future Developments

- **Fine-tuning Features**: The addition of `finetune.py` is planned, which will introduce capabilities for model fine-tuning directly through PyGPTPrompt.
- **Expanded LLaMA Model Support**: Continued development to fully integrate and support LLaMA models, including both quantized and full-sized variants (Currently a Work in Progress).
- **Memory and Recall Enhancement**: Ongoing improvements to memory mechanisms, aiming to provide more sophisticated and nuanced recall abilities for models.
- **Interface and Usability Enhancements**: Regular updates to the user interface and overall usability of the tool, ensuring a smooth and intuitive experience.

This documentation reflects the current capabilities and future directions of PyGPTPrompt. As the project evolves, further updates and new features will be continuously integrated to enhance its functionality and user experience.
