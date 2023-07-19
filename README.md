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

Please note that the application is currently in a broken and incomplete state.
The developer is actively working on separating concerns for handling the APIs and
related models. There are ongoing efforts to implement freezing and unfreezing
portions of the sequences, and to fit the APIs so they are congruent and
interchangeable, supporting hot-swapping between the OpenAI API and Llama.Cpp
API. The core aspects of the library have been restructured and reorganized for
better organization, efficiency, and performance.

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
  efficient management of context windows, enhancing the short-term memory
  performance of AI models.

- **Data Ingestion:** It simplifies the process of feeding data into AI models,
  enhancing their long-term memory performance.

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

- **Context Management:** Improvements are being made to the handling of read
  commands to prevent context flooding and accidental flushing of successful
  floods. Instead of overwhelming the user with large amounts of data, the
  system will return a string indicating that the contents are too large.

- **Context Window Control:** Commands are being developed for handling the
  context window, such as freezing and unfreezing select messages within the
  queue. This will give users more control over the information they are
  interacting with.

- **Vector Database Integration:** Work is being done to implement a vector
  database to prevent the model from "forgetting" as easily. This feature will
  depend on the accuracy of the query and what's fed back into the model.

Here are some of the planned features for future development:

- **Enhanced Security Features:** Future updates will include enhanced security
  features for reading and writing files, ensuring that user data is handled
  safely and securely.

- **Third-Party API Integration:** Plans are in place to integrate with more
  third-party APIs and services, expanding the capabilities and usefulness of
  PyGPTPrompt.

If you have any feedback, ideas, or suggestions for these planned features, or
any new ones, please feel free to share them!

## Updates

As of July 19, 2023, several major changes and updates have been made:

1. **Revision Number Update:** The revision number has been updated to prepare
   for the upcoming release.

2. **OpenAI API Key Registration Fix:** The OpenAI API key registration process
   has been fixed, ensuring smoother integration.

3. **Installation Instructions Improvement:** The installation instructions have
   been enhanced for easier setup.

4. **Configuration Files Directory Path Fix:** The directory path for
   configuration files has been updated to ensure consistency.

5. **Introduction of Helper Script for Running GPT Chat Sessions:** A new helper
   script, `gptprompt.sh`, has been added to facilitate running GPT chat
   sessions.

6. **API Interface Refactoring:** The API interface has been refactored to match
   the Llama API, facilitating a smoother integration between the two.

7. **Deprecation of Chat Module:** The chat module has been deprecated and
   replaced with model-specific tools for better performance and efficiency.

8. **Addition of Model Functions Skeleton:** A skeleton for model functions has
   been added, laying the groundwork for future development.

9. **Fixes and Improvements in Configuration Management:** Several fixes and
   improvements have been made in the configuration management, including the
   addition of config for PyTorch, fixing the Llama.cpp provider, and adding
   tests for path evaluation.

10. **Refactoring of Settings:** The settings have been restructured and
    reorganized by group for better management and ease of use.

For more detailed information, you can refer to the individual commits in the
[GitHub Commits](https://github.com/teleprint-me/py.gpt.prompt/commits/main)
section.
