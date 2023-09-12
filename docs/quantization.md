# Quantization Process for Llama.Cpp Compatible Models

## Step 1: Download the Model

To download the model, use the following command:

```sh
python -m pygptprompt.download --repo_id "ehartford/Samantha-1.11-CodeLlama-34b" --local_dir "models/ehartford/Samantha-1.11-CodeLlama-34b"
```

- This command utilizes the `pygptprompt.download` Python module to fetch the
  model data.
- `--repo_id` specifies the repository ID of the model you want to download, in
  this case, "ehartford/Samantha-1.11-CodeLlama-34b."
- `--local_dir` indicates the local directory where the downloaded model will be
  stored.

## Step 2: Convert the Model

After downloading, convert the model with the following command:

```sh
python -m pygptprompt.convert models/ehartford/Samantha-1.11-CodeLlama-34b --outtype f16
```

- This command uses the `pygptprompt.convert` module to convert the downloaded
  model.
- `models/ehartford/Samantha-1.11-CodeLlama-34b` specifies the path to the
  downloaded model directory.
- `--outtype f16` indicates that the converted model should use 16-bit
  floating-point precision.

## Step 3: Quantize the Model

Quantize the converted model using the following command:

```sh
python -m pygptprompt.quantize models/ehartford/Samantha-1.11-CodeLlama-34b/ggml-model-f16.gguf --q_type q4_1
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

---

## Modifying the JSON Configuration File

To configure your model for use, modify the JSON configuration file located at
`tests/config.sample.json`. Here's how to do it:

1. Open the `config.sample.json` file using a text editor of your choice.

2. Locate the section of the JSON file that corresponds to the `llama_cpp`
   provider. It should look something like this:

   ```json
   "llama_cpp": {
     "provider": "llama_cpp",
     "model": {
       "repo_id": "teleprint-me/llama-2-7b-chat-GGUF",
       "filename": "llama-2-7b-chat.GGUF.q5_0.bin",
       "local": "models/ehartford/Samantha-1.11-CodeLlama-34b/Samantha-1.11-CodeLlama-34b.GGUF.q4_1.bin",
       // Other properties...
     }
   }
   ```

3. Update the `local` key under the `model` section to specify the path of your
   local model file. For example:

   - Update `"local"` to point to the path of your local model file.

4. Save the changes to the `config.sample.json` file.

5. You may also need to adjust other properties or configurations within the
   JSON file as required for your use case. Be sure to follow any specific
   instructions related to your project or setup.

Once you've made these modifications, your configuration file will be set up to
use the desired model with the `llama_cpp` provider.

---

## Running the Chat Script

To run the chat script and interact with the configured model, follow these
steps:

1. Ensure you have completed all the previous steps, including modifying the
   `config.sample.json` file as needed.

2. Open your terminal or command prompt.

3. Navigate to the directory where your chat script is located. Based on your
   previous command, it seems to be in `~/Documents/code/remote/pygptprompt`.

4. Activate your virtual environment if you haven't already by running:

   ```sh
   poetry install
   poetry shell
   ```

   Note: If you're using a different virtual environment setup, activate it
   accordingly.

5. Run the chat script using the following command:

   ```sh
   python -m pygptprompt.chat --chat tests/config.sample.json
   ```

6. After running the command, you should see the chat interface with an initial
   message from Samantha:

   ```
   2023-09-12 00:06:18,161 - INFO - json.py:68 - JSON successfully loaded into memory
   2023-09-12 00:06:18,161 - INFO - llama_cpp.py:91 - Using local model at models/ehartford/Samantha-1.11-CodeLlama-34b/Samantha-1.11-CodeLlama-34b.GGUF.q4_1.bin
   system
   My name is Samantha. I am a helpful assistant.

   user
   >
   ```

7. You can now start interacting with Samantha by typing your questions or
   prompts after the `>` symbol. For example:

   ```
   user
   > What is the weather like today?
   ```

   Samantha will respond to your questions and prompts based on the configured
   model and settings.

8. When you're done with the chat, remember to deactivate the virtual
   environment:

   ```sh
   deactivate
   ```

That's it! You've successfully configured, modified, and run the chat script
with the desired model.
