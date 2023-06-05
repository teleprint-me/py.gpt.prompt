#!/usr/bin/env bash

GPT_CONFIG_PATH="${HOME}/.local/share/pygptprompt"
GPT_CONFIG_FILE="${GPT_CONFIG_PATH}/config.json"
GPT_CONFIG_ENV="${GPT_CONFIG_PATH}/env"
GPT_CONFIG_URL="https://raw.githubusercontent.com/teleprint-me/py.gpt.prompt/main/tests/config.sample.json"

# Check if python is available
if ! command -v python >/dev/null 2>&1; then
    echo "Python is required but it's not installed. Please install Python and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip >/dev/null 2>&1; then
    echo "pip is required but it's not installed. Please install pip and try again."
    exit 2
fi

# Check if configuration path exists
if [ ! -d "${GPT_CONFIG_PATH}" ]; then 
    mkdir -vp "${GPT_CONFIG_PATH}"
fi

# Check if configuration file exists
if [ ! -f "${GPT_CONFIG_FILE}" ]; then
    if curl "${GPT_CONFIG_URL}" -o "${GPT_CONFIG_FILE}"; then
        echo "Sample configuration file downloaded successfully."
    else
        echo "Failed to download the sample configuration file. Please check your internet connection or try again later."
        exit 3
    fi
    echo "PyGPTPromptPath: Setup your configuration file: \$EDITOR ${GPT_CONFIG_FILE}"
    echo "PyGPTPromptInfo: Run this script again after you've set up your \`config.json\`."
    exit 4
fi

# Check if environment file exists
if [ ! -f "${GPT_CONFIG_ENV}" ]; then
    echo "PyGPTPromptEnv: Setup your environtment file: touch ${GPT_CONFIG_ENV} && \$EDITOR ${GPT_CONFIG_ENV}"
    echo "PyGPTPromptInfo: Run this script again after you've set up your \`env\`."
    exit 5
fi

# Check if pygptprompt is installed
if ! python -c "import pygptprompt" >/dev/null 2>&1; then
    echo "The pygptprompt module is not installed. Installing using \`pip --user\`:"
    pip install --user --upgrade git+https://github.com/teleprint-me/py.gpt.prompt.git
fi

# Run pygptprompt
python -m pygptprompt.main --config "${GPT_CONFIG_FILE}"
