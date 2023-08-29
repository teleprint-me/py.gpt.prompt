#!/bin/bash

# scripts/llama_download.sh

# Initialize associative arrays to hold model information
declare -A llama_shards
declare -A llama_models
declare -A code_shards
declare -A code_models

# Function to populate the llama_shards and llama_models arrays
populate_llama_models() {
    llama_shards["7B"]=0
    llama_models["7B"]="llama-2-7b"
    llama_shards["7B-chat"]=0
    llama_models["7B-chat"]="llama-2-7b-chat"
    llama_shards["13B"]=1
    llama_models["13B"]="llama-2-13b"
    llama_shards["13B-chat"]=1
    llama_models["13B-chat"]="llama-2-13b-chat"
    llama_shards["70B"]=7
    llama_models["70B"]="llama-2-70b"
    llama_shards["70B-chat"]=7
    llama_models["70B-chat"]="llama-2-70b-chat"
}

# Function to populate the code_shards and code_models arrays
populate_code_models() {
    code_shards["7b"]=0
    code_models["7b"]="CodeLlama-7b"
    code_shards["13b"]=1
    code_models["13b"]="CodeLlama-13b"
    code_shards["34b"]=3
    code_models["34b"]="CodeLlama-34b"
    code_shards["7b-Python"]=0
    code_models["7b-Python"]="CodeLlama-7b-Python"
    code_shards["13b-Python"]=1
    code_models["13b-Python"]="CodeLlama-13b-Python"
    code_shards["34b-Python"]=3
    code_models["34b-Python"]="CodeLlama-34b-Python"
    code_shards["7b-Instruct"]=0
    code_models["7b-Instruct"]="CodeLlama-7b-Instruct"
    code_shards["13b-Instruct"]=1
    code_models["13b-Instruct"]="CodeLlama-13b-Instruct"
    code_shards["34b-Instruct"]=3
    code_models["34b-Instruct"]="CodeLlama-34b-Instruct"
    # Add more code models and their corresponding information here
}

# Common Functions

get_presigned_url() {
    read -rp "Enter the URL from email: " PRESIGNED_URL
    echo "${PRESIGNED_URL}"
}

get_target_folder() {
    read -rp "Enter the target folder to download the files to (default: ./models): " TARGET_FOLDER
    if [[ -z "${TARGET_FOLDER}" ]]; then
        TARGET_FOLDER="./models"
    fi
    mkdir -p "${TARGET_FOLDER}" || {
        echo "Could not create target folder! Exiting."
        exit 1
    }
    echo "${TARGET_FOLDER}"
}

get_llama_models() {
    local LLAMA_MODELS="7B,13B,70B,7B-chat,13B-chat,70B-chat"
    read -rp "Enter the list of llama models to download without spaces (${LLAMA_MODELS}), or press Enter for all: " LLAMA_MODEL_SIZE
    if [[ -z "${LLAMA_MODEL_SIZE}" ]]; then
        LLAMA_MODEL_SIZE="${LLAMA_MODELS}"
    fi
    echo "${LLAMA_MODEL_SIZE}"
}

get_code_models() {
    local CODE_MODELS="7b,13b,34b,7b-Python,13b-Python,34b-Python,7b-Instruct,13b-Instruct,34b-Instruct"
    read -rp "Enter the list of code models to download without spaces (${CODE_MODELS}), or press Enter for all: " CODE_MODEL_SIZE
    if [[ -z "${CODE_MODEL_SIZE}" ]]; then
        CODE_MODEL_SIZE="${CODE_MODELS}"
    fi
    echo "${CODE_MODEL_SIZE}"
}

# Function for downloading models
download_model() {
    model_type=$1
    signed_url=$2

    if [[ -z "$model_type" || -z "$signed_url" ]]; then
        echo "Missing arguments to download_model function."
        exit 1
    fi

    # Downloading the model
    echo "Downloading $model_type model..."
    curl -O "$signed_url" || {
        echo "Download failed! Exiting."
        exit 1
    }
}

# Function for displaying the main menu
display_main_menu() {
    echo "Which model would you like to download?"
    echo "1. Llama Model"
    echo "2. Code Model"
    echo "3. Quit"
}

# Call the functions to populate the model arrays
populate_llama_models
populate_code_models

# Example of how to call the common functions to set initial variables
PRESIGNED_URL=$(get_presigned_url)
echo "Presigned URL: ${PRESIGNED_URL}"

# Main Script Loop for User Interaction
while :; do
    display_main_menu
    read -r choice

    case "$choice" in
        1) # Llama Model
            selected_models=$(get_llama_models)
            model_array=("${selected_models//,/ }")
            for model in "${model_array[@]}"; do
                if [[ -n "${llama_models[$model]}" ]]; then
                    download_and_validate "$model"
                else
                    echo "Invalid Llama model: $model"
                fi
            done
            ;;
        2) # Code Model
            selected_models=$(get_code_models)
            model_array=("${selected_models//,/ }")
            for model in "${model_array[@]}"; do
                if [[ -n "${code_models[$model]}" ]]; then
                    download_and_validate "$model"
                else
                    echo "Invalid Code model: $model"
                fi
            done
            ;;
        3)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac

    read -rp "Would you like to download another model? [Y/n]: " continue_choice
    if [[ "$continue_choice" =~ ^[Nn]$ ]]; then
        echo "Exiting."
        exit 0
    fi
done
