📝 This project and its contents were created with the assistance of OpenAI's GPT-3.5 and GPT-4.

# PyGPTPrompt

PyGPTPrompt is a Python interface for the OpenAI REST API that enables automation of GPT-specific tasks using prompts.

**Note:** Please be aware that this project is currently in an experimental prototype phase and has certain limitations. While the project works well in isolation, it is not yet considered production-ready.

## Overview

PyGPTPrompt is a Python-based project that provides a sandbox environment for executing interactive commands. It offers enhanced security features to restrict access to sensitive directories, ensuring a controlled execution environment.

## Features

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

The package provides a command-line interface (CLI) for interacting with the GPT model. You can start the prompt interface by running the following command:

```sh
python main.py
```

Within the prompt interface, you can issue various commands and options to interact with the GPT model. To view a list of available commands and options, use the `/help` command.

If your configuration file is not located in the current working directory, you can specify its location using the `--config` option. For example:

```sh
python main.py --config /path/to/config.json
```

This ensures that the application knows where to find your configuration file.

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

While PyGPTPrompt is still in its prototype phase, I have future plans for its development. Here are some of the features I plan to implement in the future:

-   Enhanced security features for reading and writing files.
-   Integration with more third-party APIs and services.

I welcome feedback and ideas on these planned features, as well as suggestions for new ones!

## Updates

As of May 29, 2023, several major changes and updates have been made:

1. **RSS Feed Handling:** The `RSSHandler` class has been refactored to handle fetching, parsing, and caching of RSS feeds. This includes error handling for cases where the provided URL is not an RSS feed.

2. **Content Size Handling:** The `SessionQueueProxy` now includes a `handle_content_size` method that checks if the content size exceeds the `base_limit`. If it does, a message indicating that the content has been saved to a file is returned. This method is used in the `RobotsFetcher`, `WebsiteFetcher`, and `RSSHandler` classes.

3. **Command Interpreter Cleanup:** Deprecated methods for handling large results have been removed from the `CommandInterpreter` class.

4. **Security and Bug Fixes:** Several security and bug fixes have been implemented. These include improvements to command result printing, command policy enforcement, and handling policy enforcement for traversable paths. The `SessionContext` has been refactored for a cleaner `main_loop`.

5. **Command Interpreter Implementation:** A new `CommandInterpreter` has been added for parsing and executing commands. The `/help` command has been enhanced to provide detailed information on individual commands. The `browse`, `list`, `session`, `rss`, and `process` commands have been updated for better functionality.

6. **Refactoring and Improvements:** The 'chat' package has been refactored into 'session' for better description of behavior. A new `FormatText` class has been introduced for configurable text formatting. The `SessionContext` class has been updated to integrate new classes and manage user interactions.

7. **Path Access Control:** The `allowed_paths` and `disallowed_paths` in the configuration now control access to file paths. Any subdirectories or files within the allowed paths are implicitly allowed, unless they are explicitly disallowed.

8. **Help Message Update:** The help message (`/help` command) has been updated to reflect these changes and provide clear, concise explanations of the available commands.

You can look at the following path to see the latest commits: [GitHub Commits](https://github.com/teleprint-me/py.gpt.prompt/commits/main)
