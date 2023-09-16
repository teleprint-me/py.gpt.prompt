## Developer Installation

The package can be installed using [Poetry](https://python-poetry.org/), a
Python dependency management and packaging tool. Follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/teleprint-me/py.gpt.prompt.git
   ```

2. Navigate into the project directory:

   ```sh
   cd py.gpt.prompt
   ```

3. Install Poetry using pipX:

   ```sh
   # Learn more: https://pypa.github.io/pipx/
   pip install --user --upgrade pipx
   # pipx runs each package in isolation.
   pipx install poetry
   ```

3. Install the dependencies using Poetry:

   ```sh
   # Streamlines virtual environment for easy deployment.
   # Learn more at https://python-poetry.org/docs/
   poetry install
   ```

4. Update the dependencies using Poetry:

   ```sh
   # updates the poetry lock and installs latest packages
   poetry update
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
   cp tests/config.dev.json config.json
   ```
