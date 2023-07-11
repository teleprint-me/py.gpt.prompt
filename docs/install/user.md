## User Installation

It's important to use a virtual environment to isolate the dependencies of
PyGPTPrompt from other Python projects on your system. Here's how to set up a
virtual environment using `pipx` and `poetry`:

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

4. [Obtain an API key](https://platform.openai.com/account/api-keys) from the
   [Official OpenAI Platform](https://platform.openai.com/docs/introduction/overview)
   and set it as an environment variable:

   ```sh
   echo "OPENAI_API_KEY='API_KEY_GOES_HERE'" > .env
   ```

5. Set up your configuration by downloading the sample configuration file and
   modifying it to suit your needs:

   ```sh
   curl https://raw.githubusercontent.com/teleprint-me/py.gpt.prompt/main/tests/config.sample.json -o config.json
   ```

These instructions should help end users set up a virtual environment, install
PyGPTPrompt, and configure the application to work with the OpenAI API.
