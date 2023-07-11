# Quickstart Guide

The PyGPTPrompt package provides a command-line interface (CLI) for interacting
with the GPT model. You can start the prompt interface by running the followin g
command:

```sh
python -m pygptprompt.main
```

Within the prompt interface, you can issue various commands and options to
interact with the GPT model. To view a list of available commands and options,
use the `/help` command.

If your configuration file is not located in the current working directory, you
can specify its location using the `--config` option. For example:

```sh
python -m pygptprompt.main --config /path/to/config.json
```

This ensures that the application knows where to find your configuration file.

### Keybindings

PyGPTPrompt comes with default keybindings that you can use to interact with the
application. Here's a brief overview of the available keybindings:

- `Ctrl-C`: Exits the application.
- `Ctrl-D`: Exits the application.
- `Return`: Enters a newline.
- `Alt-Return`: Submits a message (Win & Linux).
- `Option-Return`: Submits a message (Mac OS X).
- `Up/Down arrow keys`: Navigates through command history.
- `Ctrl-Shift-V`: Pastes from the system clipboard.
- `Tab`: Auto-completes commands and arguments. (TODO)

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
