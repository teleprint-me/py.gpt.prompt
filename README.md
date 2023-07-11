📝 This project and its contents were created with the assistance of OpenAI's
GPT-3.5 and GPT-4.

# PyGPTPrompt

PyGPTPrompt is a CLI tool designed to enhance user interactions with advanced AI
models. It specializes in managing context windows, optimizing the long-term
memory performance of models like OpenAI's GPT-3.5, GPT-4, and those supported
by the llama.cpp Python API. By streamlining data ingestion and facilitating
task automation, PyGPTPrompt serves as an effective interface for AI model
interaction.

![GPT-3.5 Turbo Demo](docs/assets/gpt-3.5-turbo.gif)

## Prerequisites

- [python](https://www.python.org/) 3.10 or later
- [pipx](https://pypa.github.io/pipx/)
- [poetry](https://python-poetry.org/docs/)

- Minimum Hardware
    - Quad-Core Processor 
    - 8 GB CPU RAM
    - 6 GB GPU VRAM

- Recommended Hardware
    - Octa-Core Processor
    - 64 GB CPU RAM
    - 24 GB GPU VRAM

## Features

- **Context Window Management:** PyGPTPrompt's core functionality lies in its
  efficient management of context windows, enhancing the long-term memory
  performance of AI models.

- **Data Ingestion:** It simplifies the process of feeding data into AI models,
  further enhancing their long-term memory performance.

- **Task Automation:** PyGPTPrompt enables effective task automation with AI
  models, saving time and improving productivity.

- **Multiple Model Support:** It integrates with OpenAI and GGML models,
  supporting those quantized to 4, 5, and 8-bit variations supported by the
  llama.cpp library.

- **First-Class Support for OpenAI GPT Models:** Designed with OpenAI's GPT
  models in mind, PyGPTPrompt integrates with these AI models through their
  functions API.

- **Flexible Configuration:** Comes with comprehensive configuration files for
  customization of various parameters and settings, catering to a wide range of
  use cases and requirements.

## Development Status

PyGPTPrompt is currently in an experimental prototype phase. While functional
and showing promising potential, it is under active development and not yet
production-ready. The solo developer behind this project is committed to
refining and enhancing PyGPTPrompt, making it a versatile tool for managing AI
models' context windows and facilitating user interactions.

## Documentation

- [Read the Docs](docs/)
- [Features](docs/features.md)
- [Install](docs/install/)
- [Quickstart](docs/quickstart.md)
- [Prompting](docs/prompting/)
- [Models](docs/models/)

## Roadmap

While PyGPTPrompt is still in its prototype phase, there are several features
currently being worked on, and plans for future development. Here are some of
the features currently being worked on:

- Cleaning up read commands to prevent context flooding and accidental flushing
  of successful floods, and instead returning a string indicating that the
  contents are too large.
- Adding commands for handling the context window, such as freezing and
  unfreezing select messages within the queue.
- Implementing a vector database to prevent the model from "forgetting" as
  easily. This will depend on the accuracy of the query and what's fed back into
  the model.

Here are some of the planned features for future development:

- Enhanced security features for reading and writing files.
- Integration with more third-party APIs and services.

If you have any feedback, ideas, or suggestions for these planned features, or
any new ones, please feel free to share them!

## Updates

As of June 4, 2023, several major changes and updates have been made:

1. **Bump Revision Number:** The revision number has been bumped from 0.0.6 to
   0.0.7 to prepare for the upcoming release.

2. **Fix OpenAI API Key Registration:** The OpenAI API key registration process
   has been fixed, ensuring smoother integration.

3. **Improved Installation Instructions:** The installation instructions have
   been enhanced for easier setup.

4. **Add Shebang to main.py:** The `main.py` file now includes a shebang to make
   it an executable module.

5. **Fix Directory Path for Configuration Files:** The directory path for
   configuration files has been updated to ensure consistency.

6. **Introduce Helper Script for Running GPT Chat Sessions:** A new helper
   script, `gptprompt.sh`, has been added to facilitate running GPT chat
   sessions.

For more detailed information, you can refer to the individual commits in the
[GitHub Commits](https://github.com/teleprint-me/py.gpt.prompt/commits/main)
section.
