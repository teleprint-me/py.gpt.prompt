📝 This project and its contents were created with the assistance of OpenAI's GPT-3.5 and GPT-4.

# PyGPTPrompt

A Python interface for the OpenAI REST API to automate GPT via prompts.

## Overview

PyGPTPrompt is a Python-based project that allows for interactive command execution within a controlled environment. It provides a sandbox for executing commands, with enhanced security features that restrict access to sensitive directories.

## Features

PyGPTPrompt supports a range of commands for interacting with web pages, RSS feeds, and the local file system:

![GPT-3.5 Turbo Demo](./assets/gpt-3.5-turbo.gif)

### Web Pages

-   `/robots <url>`: Get the robots.txt of a specified URL.
-   `/browse <url>`: Fetch HTML from a specified URL, convert it to Markdown, and cache it locally. If the content already exists in the cache, it will return the cached version.

### RSS Feeds

-   `/rss <url>`: Fetch and display full text articles from an RSS feed.

### Filesystem

These commands are access restricted by configuration:

-   `/ls <dir>`: List files in a local directory. For example, `/ls Documents/` lists all files and directories within the `Documents/` directory.
-   `/read <file> [start_line] [end_line]`: Read local file content from `start_line` to `end_line` (if specified). The line numbers start at 1. For example, `/read test.txt 10 20` reads lines 10 to 20 from the `test.txt` file.
-   `/tree <directory> [--ignore dir1,dir2,...]`: Display the directory and file structure in a tree format. Optionally, ignore specified directories. For instance, `/tree /path/to/directory --ignore dir1,dir2` displays the file structure excluding `dir1` and `dir2`.
-   `/git <params>`: Access and execute local git commands. For example, `/git status` will show the current status of your git repository.

## Configurations

PyGPTPrompt uses a `config.json` file to specify a variety of settings. This includes the OpenAI GPT model to be used, maximum tokens for the model, temperature, a system message, as well as security configurations for command execution and file access.

Here is an example of how the configuration might look:

```json
{
    "model": "gpt-3.5-turbo",
    "max_tokens": 1024,
    "temperature": 0.5,
    "system_message": {
        "role": "system",
        "content": "Your name is ChatGPT. You are a pair programming assistant..."
    },
    "command_execution": {
        "shell": {
            "allowed_commands": ["ls", "cat", "cd", "git", "tree"],
            "disallowed_commands": ["rm", "sudo", "su"],
            "disallowed_strings": ["-rf /", ":(){ :|:& };:"],
            "disallowed_chars": ["&", "|", ";"]
        },
        "file_access": {
            "allowed_paths": ["/path/to/code", "/path/to/code/py.gpt.prompt"],
            "disallowed_paths": ["/path/to/code/py.gpt.prompt/.env"]
        }
    }
}
```

This update provides a more detailed explanation of each field in the configuration file and emphasizes the importance of careful configuration for security.

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

## Usage

The package offers a command-line interface (CLI) for interacting with the GPT model. You can start the prompt interface with this command:

```sh
python main.py
````

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

## Updates

As of 2023-05-16, security features have been added to the `read_file` and `list_directory` functions. This prevents access to sensitive files and directories that are not specified in the allowed paths of the configuration.

## Roadmap

While PyGPTPrompt is still in its prototype phase, I have future plans for its development. Here are some of the features I plan to implement in the future:

-   Enhanced security features for reading and writing files.
-   Integration with more third-party APIs and services.

I welcome feedback and ideas on these planned features, as well as suggestions for new ones!
