📝 This project and its contents were created with the assistance of OpenAI's GPT-3.5 and GPT-4.

# PyGPTPrompt

A Python interface for the OpenAI REST API to automate GPT via prompts.

**Note:** Please be aware that this project is still in its experimental prototype phase. It currently has certain limitations, such as handling API keys, environment variables, and configuration files, which are yet to be fully addressed. The project functions well in isolation, but it's not yet production-ready.

## Overview

PyGPTPrompt is a Python-based project that allows for interactive command execution within a controlled environment. It provides a sandbox for executing commands, with enhanced security features that restrict access to sensitive directories.

## Features

PyGPTPrompt supports a range of commands for interacting with web pages, RSS feeds, shell processes, and the local file system:

![GPT-3.5 Turbo Demo](./assets/gpt-3.5-turbo.gif)

### Web Pages

-   `/robots <url>`: Get the robots.txt of a specified URL.
-   `/browse <url>`: Fetch HTML from a specified URL, convert it to Markdown, and cache it locally. If the content already exists in the cache, it will return the cached version.

### RSS Feeds

-   `/rss <url>`: Fetch and display full text articles from an RSS feed.

### Sub-Process

-   `/<command>`: Execute a shell command (restricted by configuration).

For example:

-   `/cat <file>`: Read content from a local file.
-   `/git status`: Display the status of a git repository.

### Filesystem

Access to filesystem commands is restricted by configuration for enhanced privacy:

-   `/ls <dir>`: List files in a local directory without revealing user names, ownership, or other sensitive details. For example, `/ls Documents/` lists all files and directories within the `Documents/` directory.

## Configuration

PyGPTPrompt uses a `config.json` file to manage various settings, including the OpenAI GPT model, security configurations, and more. Here's a breakdown of each section:

### chat_completions

This section configures the chat model.

-   `model`: The name of the chat model. As of now, "gpt-3.5-turbo" is recommended.
-   `max_tokens`: The maximum number of tokens for the model to generate in a single response.
-   `temperature`: Controls the randomness of the model's output. Higher values (closer to 1) make the output more random, while lower values make it more deterministic.
-   `system_message`: The initial message that sets the behavior of the assistant.

### path

This section configures various paths used by the application.

-   `session`: The path to the directory where session data is stored.
-   `environment`: The path to the environment file.
-   `storage`: The path to the directory where the application stores its data.

### access

This section configures access controls for shell commands and file paths.

#### shell

-   `allowed_commands`: A list of shell commands that are allowed to be executed.
-   `disallowed_commands`: A list of shell commands that are explicitly disallowed.
-   `disallowed_strings`: A list of strings that, if present in a command, will cause it to be disallowed.
-   `disallowed_chars`: A list of characters that, if present in a command, will cause it to be disallowed.

#### file

-   `allowed_paths`: A list of file paths that are allowed to be accessed. Any subdirectories or files within these paths are implicitly allowed, unless they are explicitly disallowed.
-   `disallowed_paths`: A list of file paths that are explicitly disallowed. These paths take precedence over the allowed paths.

### style

This section configures the style of the output.

-   `italic`: The string to use for italic text.
-   `bold`: The string to use for bold text.

Please handle the configuration file with care. Incorrect settings, especially in the `access` section, could lead to security vulnerabilities. Always ensure that your `disallowed_paths` adequately protect sensitive files and directories, and that your `allowed_commands` do not include commands that could harm your system.

Here's an example of a `config.json` file:

```json
{
    "chat_completions": {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1024,
        "temperature": 0.5,
        "system_message": {
            "role": "system",
            "content": "Your name is ChatGPT. You are a programming assistant..."
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

This configuration provides a high degree of customization. However, it's important to handle it with care. Incorrect settings, particularly in the `access` section, could potentially lead to security vulnerabilities. Always ensure that your `disallowed_paths` adequately protect sensitive files and directories, and that your `allowed_commands` do not include commands that could harm your system.

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
    echo "OPENAI_API_KEY=<API_KEY_GOES_HERE>" > .env
    ```

## Usage

The package offers a command-line interface (CLI) for interacting with the GPT model. You can start the prompt interface with this command:

```sh
python main.py
```

In the prompt interface, you can issue various commands and options to interact with the GPT model. For a list of available commands and options, use the `/help` command.

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

As of May 26, 2023, several major changes and updates have been made:

1. **Security and Bug Fixes:** Several security and bug fixes have been implemented. These include improvements to command result printing, command policy enforcement, and handling policy enforcement for traversable paths. The `SessionContext` has been refactored for a cleaner `main_loop`.

2. **Command Interpreter Implementation:** A new `CommandInterpreter` has been added for parsing and executing commands. The `/help` command has been enhanced to provide detailed information on individual commands. The `web`, `list`, `session`, `feed`, and `process` commands have been updated for better functionality.

3. **Refactoring and Improvements:** The 'chat' package has been refactored into 'session' for better description of behavior. A new `FormatText` class has been introduced for configurable text formatting. The `SessionContext` class has been updated to integrate new classes and manage user interactions.

4. **Path Access Control:** The `allowed_paths` and `disallowed_paths` in the configuration now control access to file paths. Any subdirectories or files within the allowed paths are implicitly allowed, unless they are explicitly disallowed.

5. **Help Message Update:** The help message (`/help` command) has been updated to reflect these changes and provide clear, concise explanations of the available commands.

You can look at the following path to see the latest commits: [GitHub Commits](https://github.com/teleprint-me/py.gpt.prompt/commits/dev)
