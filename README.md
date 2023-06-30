📝 This project and its contents were created with the assistance of OpenAI's GPT-3.5 and GPT-4.

# PyGPTPrompt

PyGPTPrompt is a user-friendly CLI tool designed for managing context windows for advanced AI models, including OpenAI's GPT-3.5, GPT-4, and now also supports the llama.cpp Python API to facilitate integration of other models like the quantized spin-offs of Microsoft's Orca model. This tool streamlines user interactions and data ingestion, enabling an optimized use of the AI models' long-term memory and facilitating task automation.

**Note:** PyGPTPrompt is a passion project by a solo developer, supported by AI models for assistance. As it is currently in an experimental prototype phase, it may exhibit some limitations and areas for improvement. Despite being functional and showing significant potential in a controlled environment, it is still under active development and is not considered production-ready yet.

## Overview

PyGPTPrompt is built using Python and offers a secure sandbox environment for executing interactive commands with AI models. It comes equipped with enhanced security measures that restrict access to sensitive directories, ensuring a safe and controlled execution environment.

One of the core offerings of PyGPTPrompt is its seamless integration with advanced AI models. The tool serves as an effective interface for interaction between the user and AI models, making use of their respective Python APIs for optimal compatibility and performance.

## Features

- **Multiple Model Support:** PyGPTPrompt now supports llama.cpp's Python API, facilitating the integration of a broader range of models including a quantized spin-off of Microsoft's Orca model.

- **Context Window Management:** Efficiently manage the context windows of your AI models for streamlined interactions.
  
- **Data Ingestion:** PyGPTPrompt simplifies the process of feeding data into AI models, enhancing their long-term memory performance.

- **Task Automation:** PyGPTPrompt enables effective task automation with AI models, saving time and improving productivity.

- **Secure Execution Environment:** The tool implements advanced security features, restricting access to sensitive directories to ensure secure interactions.

- **First-Class Support for OpenAI GPT Models:** Designed with OpenAI's GPT models in mind, PyGPTPrompt integrates flawlessly with these AI models through their functions API.

## Development Status

Being a solo developer's endeavor, PyGPTPrompt is currently in an experimental prototype phase. While it is functional and shows promising potential, there are some limitations and issues that are actively being worked on. Please stay tuned for future updates and improvements as this project continues to evolve with the valuable assistance of AI models.

---

This solo developer is committed to refining and enhancing PyGPTPrompt, striving to make it a top-notch tool for managing AI models' context windows, facilitating user interactions, and optimizing data ingestion and task automation. Thank you for your patience and understanding during this development process.

## Feature Implementations

PyGPTPrompt offers the following features for interacting with various components:

![GPT-3.5 Turbo Demo](./assets/gpt-3.5-turbo.gif)

### Web Pages

-   `/robots <url>`: Fetch the robots.txt file of a specified URL.
-   `/browse <url>`: Retrieve HTML content from a specified URL, convert it to Markdown, and cache it locally. If the content already exists in the cache, the cached version is returned.

### RSS Feeds

-   `/rss <url>`: Fetch and display full-text articles from an RSS feed.

### Filesystem

-   `/ls <dir>`: List files in a local directory without revealing sensitive details. Access to filesystem commands is restricted by configuration to enhance privacy.

### Reading Files

-   `/read <file> [start_line] [end_line]`: Read the content of a local file. This command retrieves the content of the specified file, optionally specifying the range of lines to read.

### Sub-Process

-   `/<command>`: Execute a shell command (restricted by configuration).

Examples:

-   `/cat <file>`: Read the content of a local file.
-   `/git status`: Display the status of a git repository.

Please note that the available commands may be subject to configuration restrictions. For detailed information on each command, you can refer to the `/help` command.

## Configuration

PyGPTPrompt uses a `config.json` file to manage various settings, including the OpenAI GPT model, security configurations, and more. Here's a breakdown of each section:

### chat_completions

Configures the chat model used by PyGPTPrompt.

-   `model`: The name of the chat model. "gpt-3.5-turbo" is currently recommended.
-   `max_tokens`: The maximum number of tokens for the model to generate in a single response.
-   `temperature`: Controls the randomness of the model's output. Higher values (closer to 1) make the output more random, while lower values make it more deterministic.
-   `base_limit_percentage`: Represents the percentage of the context window size reserved for resulting output. Content exceeding this percentage is written to a file and its path is returned.
-   `system_message`: The initial message that sets the behavior of the assistant.

### path

Configures various paths used by PyGPTPrompt.

-   `session`: The path to the directory where session data is stored.
-   `environment`: The path to the environment file.
-   `storage`: The path to the directory where the application stores its data.

### access

Configures access controls for shell commands and file paths.

#### shell

-   `allowed_commands`: A list of allowed shell commands.
-   `disallowed_commands`: A list of explicitly disallowed shell commands.
-   `disallowed_strings`: A list of strings that, if present in a command, will cause it to be disallowed.
-   `disallowed_chars`: A list of characters that, if present in a command, will cause it to be disallowed.

#### file

-   `allowed_paths`: A list of allowed file paths. Subdirectories and files within these paths are implicitly allowed unless explicitly disallowed.
-   `disallowed_paths`: A list of explicitly disallowed file paths, taking precedence over allowed paths.

### style

Configures the style of the output.

-   `italic`: The string to use for italic text.
-   `bold`: The string to use for bold text.

Handle the configuration file with care to ensure security. Pay attention to the `access` section, ensuring that `disallowed_paths` adequately protect sensitive files and directories. Review the `allowed_commands` to exclude any potentially risky commands. Customization options are available, but it's crucial to make informed choices to maintain a secure environment.

Here's an example of a `config.json` file:

```json
{
    "chat_completions": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1024,
        "temperature": 0.5,
        "base_limit_percentage": 0.1,
        "system_message": {
            "role": "system",
            "content": "I am ChatGPT, an AI programming assistant utilizing the `pygptprompt` interactive CLI based on `prompt-toolkit`..."
        }
    },
    "path": {
        "session": "/path/to/sessions",
        "environment": "/path/to/env",
        "storage": "/path/to/storage"
    },
    "access": {
        "shell": {
            "allowed_commands": ["ls", "cat", "cd", "tree", "git"],
            "disallowed_commands": ["rm", "sudo", "su"],
            "disallowed_strings": ["-rf /", ":(){ :|:& };:"],
            "disallowed_chars": ["&", "|", ";", "*", ">"]
        },
        "file": {
            "allowed_paths": ["/path/to/source/code", "/path/to/files"],
            "disallowed_paths": [
                "/path/to/env",
                "/path/to/private/keys",
                "/path/to/config.json"
            ]
        }
    },
    "style": {
        "italic": "italic",
        "bold": "bold"
    }
}
```

## Prerequisites

-   Python 3.11 or later
-   Poetry (Python packaging and dependency management tool)

## Installation

### End User

It's important to use a virtual environment to isolate the dependencies of PyGPTPrompt from other Python projects on your system. Here's how to set up a virtual environment using `pipx` and `poetry`:

1. Install `pipx` and `poetry`:

    ```sh
    # pipx runs each package in isolation.
    # Learn more at https://github.com/pipxproject/pipx
    pip install --user --upgrade pipx
    pipx install poetry
    ```

    Alternatively, you can install PyGPTPrompt using `virtualenv`:

    ```sh
    virtualenv .venv
    source .venv/bin/activate
    pip install git+https://github.com/teleprint-me/py.gpt.prompt.git
    pip freeze > requirements.txt
    ```

    Then skip step 2 and continue from step 3 if you opted for `virtualenv`.

2. Create, activate, and install using `poetry`:

    ```sh
    poetry init  # follow the prompts
    poetry shell
    poetry add git+https://github.com/teleprint-me/py.gpt.prompt.git
    ```

3. Setup `git` and your `.gitignore`

    ```sh
    git init
    curl https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o .gitignore
    git add .gitignore  # add /sessions and /storage if they're local
    git commit -s -m "Initial commit" .gitignore
    ```

4. [Obtain an API key](https://platform.openai.com/account/api-keys) from the [Official OpenAI Platform](https://platform.openai.com/docs/introduction/overview) and set it as an environment variable:

    ```sh
    echo "OPENAI_API_KEY='API_KEY_GOES_HERE'" > .env
    ```

5. Set up your configuration by downloading the sample configuration file and modifying it to suit your needs:

    ```sh
    curl https://raw.githubusercontent.com/teleprint-me/py.gpt.prompt/main/tests/config.sample.json -o config.json
    ```

These instructions should help end users set up a virtual environment, install PyGPTPrompt, and configure the application to work with the OpenAI API.

### Development

The package can be installed using [Poetry](https://python-poetry.org/), a Python dependency management and packaging tool. Follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/teleprint-me/py.gpt.prompt.git
    ```

2. Navigate into the project directory:

    ```sh
    cd py.gpt.prompt
    ```

3. Install the dependencies using Poetry:

    ```sh
    # pipx runs each package in isolation.
    # Learn more at https://github.com/pipxproject/pipx
    pip install --user --upgrade pipx
    pipx install poetry
    poetry install
    ```

4. Activate the environment.

    ```sh
    poetry shell
    ```

5. Setup your API Key.

    ```sh
    echo "OPENAI_API_KEY='API_KEY_GOES_HERE'" > .env
    ```

6. Setup your configuration.

    ```sh
    cp tests/config.example.json config.json
    ```

## Usage

The PyGPTPrompt package provides a command-line interface (CLI) for interacting with the GPT model. You can start the prompt interface by running the followin
g command:

```sh
python -m pygptprompt.main
```

Within the prompt interface, you can issue various commands and options to interact with the GPT model. To view a list of available commands and options, use
the `/help` command.

If your configuration file is not located in the current working directory, you can specify its location using the `--config` option. For example:

```sh
python -m pygptprompt.main --config /path/to/config.json
```

This ensures that the application knows where to find your configuration file.

### Keybindings

PyGPTPrompt comes with default keybindings that you can use to interact with the application. Here's a brief overview of the available keybindings:

-   `Ctrl-C`: Exits the application.
-   `Ctrl-D`: Exits the application.
-   `Return`: Enters a newline.
-   `Alt-Return`: Submits a message (Win & Linux).
-   `Option-Return`: Submits a message (Mac OS X).
-   `Up/Down arrow keys`: Navigates through command history.
-   `Ctrl-Shift-V`: Pastes from the system clipboard.
-   `Tab`: Auto-completes commands and arguments. (TODO)

## Example Session

Here is an actual transcript of a session using the application:

```sh
(py-gpt-prompt-py3.11) ➜  py.gpt.prompt git:(main) ✗ python main.py
Enter a name for the session: test
```

### Session: test

```sh
system
Your name is GPT. You are a pair programming assistant. You have access to special commands. Use `/help` for more information...

user
Hello!

assistant
Hello! How can I assist you today?

user
We need to test the command system. Let's start with /help...

...[conversation continues]...

user
/git status

assistant
It looks like you ran the `/git status` command. The output shows that you have made changes to some files and those changes are yet to be committed. Additionally, it also suggests that your local branch is ahead of the 'origin/main' branch by one commit. Please consider committing your changes by running the `git commit` command and push them to the remote branch using `git push`, if you haven't already.
```

## Roadmap

While PyGPTPrompt is still in its prototype phase, there are several features currently being worked on, and plans for future development. Here are some of the features currently being worked on:

-   Cleaning up read commands to prevent context flooding and accidental flushing of successful floods, and instead returning a string indicating that the contents are too large.
-   Adding commands for handling the context window, such as freezing and unfreezing select messages within the queue.
-   Implementing a vector database to prevent the model from "forgetting" as easily. This will depend on the accuracy of the query and what's fed back into the model.

Here are some of the planned features for future development:

-   Enhanced security features for reading and writing files.
-   Integration with more third-party APIs and services.

If you have any feedback, ideas, or suggestions for these planned features, or any new ones, please feel free to share them!

## Updates

As of June 4, 2023, several major changes and updates have been made:

1. **Bump Revision Number:** The revision number has been bumped from 0.0.6 to 0.0.7 to prepare for the upcoming release.

2. **Fix OpenAI API Key Registration:** The OpenAI API key registration process has been fixed, ensuring smoother integration.

3. **Improved Installation Instructions:** The installation instructions have been enhanced for easier setup.

4. **Add Shebang to main.py:** The `main.py` file now includes a shebang to make it an executable module.

5. **Fix Directory Path for Configuration Files:** The directory path for configuration files has been updated to ensure consistency.

6. **Introduce Helper Script for Running GPT Chat Sessions:** A new helper script, `gptprompt.sh`, has been added to facilitate running GPT chat sessions.

For more detailed information, you can refer to the individual commits in the [GitHub Commits](https://github.com/teleprint-me/py.gpt.prompt/commits/main) section.
