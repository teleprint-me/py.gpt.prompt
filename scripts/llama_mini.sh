#!/bin/bash

# Function to download the model
download_model() {
    model_size=$1
    output_dir=$2
    output_file=$3

    # URL for the model
    url="https://karpathy.ai/llama2c/$output_file"

    # Google Drive backup URL
    backup_url="https://drive.google.com/file/d/1aTimLdx3JktDXxcHySNrZJOOk8Vb1qBR/view?usp=share_link"

    # Create the output directory if it doesn't exist
    mkdir -p $output_dir

    # Try to download the model
    wget $url -O $output_dir/$output_file

    # If wget fails, try to download from the backup URL
    if [ $? -ne 0 ]; then
        echo "Failed to download from $url, trying backup URL..."
        wget $backup_url -O $output_dir/$output_file
    fi
}

# Ask the user which model they want to download
echo "Which model do you want to download? (15M/44M)"
read model_size

# Set the output directory and file based on the chosen model size
if [ "$model_size" == "15M" ]; then
    output_dir="models/llama2-mini-15M"
    output_file="model.bin"
elif [ "$model_size" == "44M" ]; then
    output_dir="models/llama2-mini-44M"
    output_file="model44m.bin"
else
    echo "Invalid model size. Please choose either 15M or 44M."
    exit 1
fi

# Download the chosen model
download_model $model_size $output_dir $output_file
