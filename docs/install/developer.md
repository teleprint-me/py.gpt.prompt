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
