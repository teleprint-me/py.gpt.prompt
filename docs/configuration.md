# Configuration

This document provides an overview and description of the configuration file
used in the project.

## App Configuration

### Path Configuration

The `app.path` section defines the paths used by the application:

- `local`: The local path for storing PyGPTPrompt data. Default:
  `${HOME}/.local/share/pygptprompt`
- `cache`: The cache path for PyGPTPrompt. Default: `${HOME}/.cache/pygptprompt`
- `config`: The configuration path for PyGPTPrompt. Default:
  `${HOME}/.config/pygptprompt`

### Access Configuration

The `app.access` section controls access settings for the application:

- `confirm`: A boolean value indicating whether access confirmation is required.
  Default: `true`
- `shell.allowed_commands`: An array of allowed shell commands. Default:
  `["date", "cal", "pwd", "cat", "grep", "git", "tree", "virtualenv", "poetry", "pytest"]`
- `shell.disallowed_commands`: An array of disallowed shell commands. Default:
  `["rm", "sudo", "su"]`
- `shell.disallowed_strings`: An array of disallowed strings in shell commands.
  Default: `["-rf /", ":(){ :|:& };:"]`
- `shell.disallowed_chars`: An array of disallowed characters in shell commands.
  Default: `["&", ";", "*", ">", ">>", "|"]`
- `file.allowed_paths`: An array of allowed file paths. Default:
  `["${PWD}", "${HOME}/.cache/pygptprompt"]`
- `file.disallowed_paths`: An array of disallowed file paths. Default:
  `[".env", "${HOME}/.config/pygptprompt"]`

### Style Configuration

The `app.style` section defines the styling options for the application:

- `italic`: The style for italic text. Default: `italic`
- `bold`: The style for bold text. Default: `bold`

## Embedding Configuration

The `embedding` section specifies the embedding settings for the application:

- `device`: The device to use for embedding. Default: `cpu`
- `model`: The model to use for embedding. Default: `hkunlp/instructor-large`
- `function`: The embedding function to use. Default:
  `InstructorEmbeddingFunction`

## LLAMA CPP Configuration

The `llama_cpp` section contains configuration options for LLAMA CPP:

- `provider`: The provider for LLAMA CPP. Default: `huggingface`
- `model.repo_id`: The repository ID for the LLAMA CPP model. Default:
  `TheBloke/orca_mini_7B-GGML`
- `model.filename`: The filename of the LLAMA CPP model. Default:
  `orca-mini-7b.ggmlv3.q5_1.bin`
- `model.n_ctx`: The number of context tokens for the LLAMA CPP model. Default:
  `512`
- `model.n_parts`: The number of model parts to use. Default: `-1`
- `model.seed`: The seed value for the LLAMA CPP model. Default: `1337`
- `model.f16_kv`: Use half-precision (float16) for key-value embeddings.
  Default: `true`
- `model.logits_all`: Output logits for all tokens instead of just the last
  token. Default: `false`
- `model.vocab_only`: Use vocabulary embeddings only. Default: `false`
- `model.use_mmap`: Use mmap to load the LLAMA CPP model. Default: `true`
- `model.use_mlock`: Lock the model in memory. Default: `false`
- `model.embedding`: Enable embedding functionality. Default: `true`
- `model.n_threads`: The number of threads to use. Default: `null`
- `model.n_batch`: The batch size for LLAMA CPP. Default: `512`
- `model.last_n_tokens_size`: The size of the last n tokens for LLAMA CPP.
  Default: `64`
- `model.lora_base`: The base path for Lora model parts. Default: `null`
- `model.lora_path`: The path for Lora model parts. Default: `null`
- `model.tensor_split`: The tensor split strategy for LLAMA CPP. Default: `null`
- `model.rope_freq_base`: The base frequency for rope data. Default: `10000.0`
- `model.rope_freq_scale`: The frequency scale for rope data. Default: `1.0`
- `model.verbose`: Enable verbose logging for LLAMA CPP. Default: `false`

The `chat_completions` subsection specifies the settings for chat completions:

- `max_tokens`: The maximum number of tokens to generate in chat completions.
  Default: `512`
- `temperature`: The temperature for chat completions. Default: `0.8`
- `top_p`: The top-p probability cutoff for chat completions. Default: `0.95`
- `top_k`: The top-k token sampling cutoff for chat completions. Default: `40`
- `stream`: Enable streaming of chat completions. Default: `true`
- `stop`: An array of stop tokens to stop generation. Default: `[]`
- `repeat_penalty`: The repeat penalty for chat completions. Default: `1.1`

The `context` subsection controls the context settings for LLAMA CPP:

- `reserve`: The amount of context to reserve for LLAMA CPP. Default: `0.2`

The `system_prompt` subsection defines the system prompt for LLAMA CPP:

- `role`: The role of the system prompt. Default: `system`
- `content`: The content of the system prompt. Default:
  `My name is Orca. I am a helpful programming assistant.`

## OpenAI Configuration

The `openai` section contains configuration options for OpenAI:

- `provider`: The provider for OpenAI. Default: `openai`

The `chat_completions` subsection specifies the settings for chat completions:

- `model`: The model to use for chat completions. Default: `gpt-3.5-turbo`
- `temperature`: The temperature for chat completions. Default: `0.8`
- `max_tokens`: The maximum number of tokens to generate in chat completions.
  Default: `512`
- `top_p`: The top-p probability cutoff for chat completions. Default: `0.95`
- `n`: The number of completions to generate. Default: `1`
- `stream`: Enable streaming of chat completions. Default: `false`
- `stop`: The stop sequence for chat completions. Default: `null`
- `presence_penalty`: The presence penalty for chat completions. Default: `0`
- `frequency_penalty`: The frequency penalty for chat completions. Default: `0`
- `logit_bias`: The logit bias for chat completions. Default: `null`

The `embeddings` subsection specifies the model for text embeddings:

- `model`: The model to use for text embeddings. Default:
  `text-embedding-ada-002`

## Function Configuration

The `function` section contains definitions for custom functions:

- `name`: The name of the function. Example: `get_current_weather`
- `description`: The description of the function. Example:
  `Get the current weather in a given location`
- `parameters`: The parameters of the function. Example:
  `{ "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "unit": { "type": "string", "enum": ["celsius", "fahrenheit"] } }`
