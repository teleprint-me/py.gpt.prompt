#!/bin/bash

# scripts/llama_download.sh

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

# Example of how to call the common functions to set initial variables
PRESIGNED_URL=$(get_presigned_url)
echo "Presigned URL: ${PRESIGNED_URL}"

# Main Script Loop for User Interaction
while :; do
    display_main_menu
    read -r choice

    case $choice in
    1)
        LLAMA_MODEL_SIZE=$(get_llama_models)
        echo "Llama Model Size: ${LLAMA_MODEL_SIZE}"
        download_model "Llama" "${PRESIGNED_URL}"
        ;;
    2)
        CODE_MODEL_SIZE=$(get_code_models)
        echo "Code Model Size: ${CODE_MODEL_SIZE}"
        download_model "Code" "${PRESIGNED_URL}"
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
