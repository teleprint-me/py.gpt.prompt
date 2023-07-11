## Prototyped Features

![GPT-3.5 Turbo Demo](assets/gpt-3.5-turbo.gif)

PyGPTPrompt offers the following features for interacting with various
components:

### Web Pages

- `/robots <url>`: Fetch the robots.txt file of a specified URL.
- `/browse <url>`: Retrieve HTML content from a specified URL, convert it to
  Markdown, and cache it locally. If the content already exists in the cache,
  the cached version is returned.

### RSS Feeds

- `/rss <url>`: Fetch and display full-text articles from an RSS feed.

### Filesystem

- `/ls <dir>`: List files in a local directory without revealing sensitive
  details. Access to filesystem commands is restricted by configuration to
  enhance privacy.

### Reading Files

- `/read <file> [start_line] [end_line]`: Read the content of a local file. This
  command retrieves the content of the specified file, optionally specifying the
  range of lines to read.

### Sub-Process

- `/<command>`: Execute a shell command (restricted by configuration).

Examples:

- `/cat <file>`: Read the content of a local file.
- `/git status`: Display the status of a git repository.

Please note that the available commands may be subject to configuration
restrictions. For detailed information on each command, you can refer to the
`/help` command.

## Configuration

PyGPTPrompt uses a `config.json` file to manage various settings, including the
OpenAI GPT model, security configurations, and more. Here's a breakdown of each
section:

### chat_completions

Configures the chat model used by PyGPTPrompt.

- `model`: The name of the chat model. "gpt-3.5-turbo" is currently recommended.
- `max_tokens`: The maximum number of tokens for the model to generate in a
  single response.
- `temperature`: Controls the randomness of the model's output. Higher values
  (closer to 1) make the output more random, while lower values make it more
  deterministic.
- `base_limit_percentage`: Represents the percentage of the context window size
  reserved for resulting output. Content exceeding this percentage is written to
  a file and its path is returned.
- `system_message`: The initial message that sets the behavior of the assistant.

### path

Configures various paths used by PyGPTPrompt.

- `session`: The path to the directory where session data is stored.
- `environment`: The path to the environment file.
- `storage`: The path to the directory where the application stores its data.

### access

Configures access controls for shell commands and file paths.

#### shell

- `allowed_commands`: A list of allowed shell commands.
- `disallowed_commands`: A list of explicitly disallowed shell commands.
- `disallowed_strings`: A list of strings that, if present in a command, will
  cause it to be disallowed.
- `disallowed_chars`: A list of characters that, if present in a command, will
  cause it to be disallowed.

#### file

- `allowed_paths`: A list of allowed file paths. Subdirectories and files within
  these paths are implicitly allowed unless explicitly disallowed.
- `disallowed_paths`: A list of explicitly disallowed file paths, taking
  precedence over allowed paths.

### style

Configures the style of the output.

- `italic`: The string to use for italic text.
- `bold`: The string to use for bold text.

Handle the configuration file with care to ensure security. Pay attention to the
`access` section, ensuring that `disallowed_paths` adequately protect sensitive
files and directories. Review the `allowed_commands` to exclude any potentially
risky commands. Customization options are available, but it's crucial to make
informed choices to maintain a secure environment.

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
