📝 This project and its contents were created with the assistance of OpenAI's
GPT-3.5 and GPT-4.

# PyGPTPrompt

PyGPTPrompt is a powerful CLI tool designed to streamline interactions with
advanced AI models. It specializes in managing context windows, optimizing both
short and long-term memory performance of models like OpenAI's GPT-3.5, GPT-4,
and those supported by the llama.cpp Python API.

![GPT-3.5 Turbo Demo](docs/assets/gpt-3.5-turbo.gif)

Please note that the application is currently under active development. The
developer is working on separating concerns for handling the APIs and related
models, implementing context window management features, and restructuring the
core aspects of the library for better organization, efficiency, and
performance.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Features](#features)
- [Development Status](#development-status)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Updates](#updates)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- [python](https://www.python.org/) 3.10 or later
- [pipx](https://pypa.github.io/pipx/)
- [poetry](https://python-poetry.org/docs/)

Hardware requirements:

- Minimum: Quad-Core Processor, 8 GB CPU RAM, 6 GB GPU VRAM
- Recommended: Octa-Core Processor, 64 GB CPU RAM, 24 GB GPU VRAM

## Features

- **Context Window Management:** Enhances the short-term memory performance of
  AI models.
- **Data Ingestion:** Simplifies feeding data into AI models, enhancing their
  long-term memory performance.
- **Task Automation:** Enables effective task automation with AI models.
- **Multiple Model Support:** Integrates with OpenAI and GGML models, supporting
  those quantized to 4, 5, and 8-bit variations supported by the llama.cpp
  library.
- **Flexible Configuration:** Comprehensive configuration files for
  customization of various parameters and settings.

## Development Status

PyGPTPrompt is currently in an experimental prototype phase. It is under active
development and not yet production-ready.

## Documentation

- [Read the Docs](docs/)
- [Features](docs/features.md)
- [Install](docs/install/)
- [Quickstart](docs/quickstart.md)
- [Prompting](docs/prompting/)
- [Models](docs/models/)

## Roadmap

- **Context Management:** Restructuring the core APIs for congruency and
  alignment to simplify hot-swapping between models and improve context
  management.
- **Context Window Control:** Implementing IRC-like commands for handling the
  context window, such as freezing and unfreezing select messages within the
  queue.
- **GPT Function Execution:** Incorporating OpenAI's new Function API features
  for more reliable retrieval of structured data.
- **Vector Database Integration:** Implementing a vector database to enhance the
  model's memory capabilities.
- **Fine-Tuning LLama-2 Models:** Creating fine-tuned Llama-2 models for
  utilizing the Functions API and improving Mathematical and Programmatic
  reasoning for chat-like interactions.

## Updates

As of July 19, 2023, several major changes and updates have been made. For more
detailed information, refer to the individual commits in the
[GitHub Commits](https://github.com/teleprint-me/py.gpt.prompt/commits/main)
section.

## Contributing

If you're interested in contributing to PyGPTPrompt, please check out the
developers contributing guidelines. The developer welcomes any form of
contribution, from bug reports to feature requests to pull requests.

## License

    A Context Window Management System for automating prompting with Chat Models.
    Copyright (C) 2023 Austin Berrio

    This program is free software: you can redistribute it and/or modify it under
    the terms of the GNU Affero General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option) any
    later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License along
    with this program. If not, see <https://www.gnu.org/licenses/>.
