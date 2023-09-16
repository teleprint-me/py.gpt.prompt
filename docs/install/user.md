## User Installation

### Use as Application

PyGPTPrompt offers a suite of CLI tools for a range of operations including OCR,
PDF-to-Text conversions, model conversions to GGUF, and model quantization to a
specified bit depth, and much more!

To use PyGPTPrompt as a standalone suite, install it using:

```sh
pip install --user --upgrade git+https://github.com/teleprint-me/py.gpt.prompt.git
```

### Use in Development

To ensure that the dependencies for PyGPTPrompt don't interfere with other
Python projects on your system, it's recommended to use a virtual environment.
Below are instructions using `pipx` and `poetry`:

1. **Install `pipx` and `poetry`**:

   ```sh
   pip install --user --upgrade pipx
   pipx install poetry
   ```

   - Learn more about [pipX](https://pypa.github.io/pipx/).

   _Alternatively, use `virtualenv`_:

   ```sh
   virtualenv .venv
   source .venv/bin/activate
   pip install git+https://github.com/teleprint-me/py.gpt.prompt.git
   pip freeze > requirements.txt
   ```

   Skip to step 3 if you opt for `virtualenv`.

2. **Initialize, Activate, and Install using `poetry`**:

   ```sh
   poetry init  # follow the prompts
   poetry shell
   poetry add git+https://github.com/teleprint-me/py.gpt.prompt.git
   ```

   - More details available in the
     [Poetry docs](https://python-poetry.org/docs/).

3. **Setup `git` and `.gitignore`**:

   ```sh
   git init
   curl https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o .gitignore
   git add .gitignore  # Optionally add /sessions and /storage if they're local
   git commit -s -m "Initial commit" .gitignore
   ```

4. **Setup OpenAI API Key**:

   [Obtain an API key](https://platform.openai.com/account/api-keys) from the
   [Official OpenAI Platform](https://platform.openai.com/docs/introduction/overview)
   and set it as an environment variable:

   ```sh
   echo "OPENAI_API_KEY='API_KEY_GOES_HERE'" > .env
   ```

   ⚠️ **Warning**: Never commit `.env` files to public repositories.

5. **Download and Edit Configuration File**:

   ```sh
   curl https://raw.githubusercontent.com/teleprint-me/py.gpt.prompt/main/tests/config.sample.json -o config.json
   ```

### Summary

These instructions should provide end-users with a comprehensive guide for
setting up a virtual environment, installing PyGPTPrompt, and configuring it to
work with the OpenAI API.
