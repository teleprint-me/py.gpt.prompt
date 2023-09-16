## Developer Installation

The package can be installed using [Poetry](https://python-poetry.org/), a
Python dependency management and packaging tool. Follow these steps:

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/teleprint-me/py.gpt.prompt.git
   ```

2. **Navigate into the Project Directory**:

   ```sh
   cd py.gpt.prompt
   ```

3. **Install Poetry Using pipX**:

   ```sh
   pip install --user --upgrade pipx
   pipx install poetry
   ```

   - Learn more about [pipX](https://pypa.github.io/pipx/).

4. **Install Dependencies Using Poetry**:

   ```sh
   poetry install
   ```

   - More details available in the
     [Poetry docs](https://python-poetry.org/docs/).

5. **Update Dependencies Using Poetry**:

   ```sh
   poetry update
   ```

6. **Activate the Environment**:

   ```sh
   poetry shell
   ```

7. **Setup Your API Key**:

   ```sh
   echo "OPENAI_API_KEY='API_KEY_GOES_HERE'" > .env
   ```

   ⚠️ **Warning**: Never commit `.env` files to public repositories.

8. **Setup Your Configuration**:
   ```sh
   cp tests/config.dev.json config.json
   ```

### Troubleshooting

- If you encounter XYZ issue, try doing ABC.
