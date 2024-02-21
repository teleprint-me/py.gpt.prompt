# Quantization Process for Llama.Cpp Compatible Models

## Step 1: Download the Model

To download the model, use the following command:

```sh
python -m pygptprompt.cli.huggingface_hub download -r ehartford/Samantha-1.11-CodeLlama-34b -p models/ehartford/Samantha-1.11-CodeLlama-34b
```

- This command utilizes the `pygptprompt.cli.huggingface_hub download` Python module to fetch the model data.
- `-r` specifies the repository ID of the model you want to download, in this case, "ehartford/Samantha-1.11-CodeLlama-34b."
- `-p` indicates the local path where the downloaded model will be stored.

## Step 2: Convert the Model

After downloading, convert the model using the `torch_to_gguf.py` script with the following command:

```sh
python -m pygptprompt.cli.convert.torch_to_gguf models/ehartford/Samantha-1.11-CodeLlama-34b --outtype f16
```

- This command uses the `torch_to_gguf.py` script to convert the downloaded model.
- `models/ehartford/Samantha-1.11-CodeLlama-34b` specifies the path to the downloaded model directory.
- `--outtype f16` indicates that the converted model should use 16-bit floating-point precision.

## Step 3: Quantize the Model

Quantize the converted model using the following command:

```sh
python -m pygptprompt.cli.quantize models/ehartford/Samantha-1.11-CodeLlama-34b/ggml-model-f16.gguf --q_type q4_1
```

- This command employs the `pygptprompt.quantize` module to perform quantization
  on the converted model.
- `models/ehartford/Samantha-1.11-CodeLlama-34b/ggml-model-f16.gguf` specifies
  the path to the converted model file.
- `--q_type q4_1` indicates the type of quantization to be applied, in this
  case, `q4_1`.

These commands provide a clear sequence for downloading, converting, and
quantizing the model, with each step contributing to reducing the model's size
and precision as needed.

## Modifying the JSON Configuration File

To configure your model for use with the `llama_cpp` provider, you'll need to modify the JSON configuration file, typically located at `tests/config.sample.json`. Follow these steps for customization:

1. **Open the Configuration File**:
   - Use a text editor of your choice to open the `config.sample.json` file.

2. **Navigate to the `llama_cpp` Section**:
   - Find the section corresponding to the `llama_cpp` provider. It usually looks like this:

     ```json
     "llama_cpp": {
       "provider": "llama_cpp",
       "model": {
         "repo_id": "teleprint-me/llama-2-7b-chat-GGUF",
         "filename": "llama-2-7b-chat.GGUF.q5_0.bin",
         "local": "models/ehartford/Samantha-1.11-CodeLlama-34b/Samantha-1.11-CodeLlama-34b.GGUF.q4_1.bin",
         // Other properties...
       },
       "system_prompt": {
         "role": "system",
         "content": "My name is Samantha. I am a helpful assistant."
       }
       // Other properties...
     }
     ```

3. **Update the `local` Key**:
   - The `"local"` key specifies the path to your local model file. If set, it overrides the automated fetching of the model using `"repo_id"` and `"filename"`. This is useful for manual control or specific model setups.
   - Example: Update the `"local"` key to point to the path of your quantized model file.

     **Note**: Use the `"local"` key for direct control over which model file to use. If omitted, PyGPTPrompt will automatically download the model specified in `"repo_id"` and `"filename"`.

4. **Adjust the System Prompt**:
   - Modify the `"content"` key under `"system_prompt"` to set the model's initial orientation and interaction style.
   - Example: Change the `"content"` to fit the context or personality of the model you're using.

5. **Save Your Changes**:
   - After making the necessary modifications, save the `config.sample.json` file.

6. **Review Other Configurations**:
   - Depending on your specific use case, you might need to adjust other properties within the JSON file. Ensure all configurations align with your project requirements.

By following these steps, you'll configure the `llama_cpp` provider to use your desired model, ensuring it operates with the correct settings and system prompt.

## Running the Chat Script

To run the chat script and interact with the configured model, follow these
steps:

1. Ensure you have completed all the previous steps, including modifying the
   `config.sample.json` file as needed.

2. Run the chat script using the following command:

   ```sh
   python -m pygptprompt.cli.chat --chat tests/config.sample.json
   ```

3. After running the command, you should see the chat interface with an initial
   message from Samantha:

   ```
   2023-09-12 00:06:18,161 - INFO - json.py:68 - JSON successfully loaded into memory
   2023-09-12 00:06:18,161 - INFO - llama_cpp.py:91 - Using local model at models/ehartford/Samantha-1.11-CodeLlama-34b/Samantha-1.11-CodeLlama-34b.GGUF.q4_1.bin
   system
   My name is Samantha. I am a helpful assistant.

   user
   >
   ```

4. You can now start interacting with Samantha by typing your questions or
   prompts after the `>` symbol. For example:

   ```
   user
   > Hello! What's your name?
   ```

   Samantha will respond to your questions and prompts based on the configured
   model and settings.

5. When you're done with the chat, remember to deactivate the virtual
   environment:

   ```sh
   deactivate
   ```

That's it! You've successfully configured, modified, and run the chat script
with the desired model.
