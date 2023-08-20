"""
pygptprompt/quantize.py

MIT License

Copyright (c) 2023 Andrei Betlen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

NOTE:
    - This is a modified script of the original example provided by Andrei Betlen.
    - I modified the original and built this script as a result alongside OpenAI's GPT-4 model(s).
    - GGML Quantization is being deprecated in favor of GGUF Quantization.
    - It is imperative that this script be treated simply as a prototype to experiment with.

Source: https://github.com/abetlen/llama-cpp-python/blob/main/examples/low_level_api/quantize.py
"""
import os

import click
from llama_cpp import (
    LLAMA_FTYPE_MOSTLY_F16,
    LLAMA_FTYPE_MOSTLY_Q4_0,
    LLAMA_FTYPE_MOSTLY_Q5_0,
    LLAMA_FTYPE_MOSTLY_Q8_0,
    llama_model_quantize,
    llama_model_quantize_default_params,
)

from pygptprompt import logging

QUANTIZATION_TYPE_KEYS = ["f16", "q8_0", "q5_0", "q4_0"]


# Mapping between user-friendly quantization type and the expected integer value
def get_quantization_type(quant_type_str):
    mapping = {
        QUANTIZATION_TYPE_KEYS[0]: LLAMA_FTYPE_MOSTLY_F16,
        QUANTIZATION_TYPE_KEYS[1]: LLAMA_FTYPE_MOSTLY_Q8_0,
        QUANTIZATION_TYPE_KEYS[2]: LLAMA_FTYPE_MOSTLY_Q5_0,
        QUANTIZATION_TYPE_KEYS[3]: LLAMA_FTYPE_MOSTLY_Q4_0,
    }
    return mapping.get(
        quant_type_str, LLAMA_FTYPE_MOSTLY_Q4_0
    )  # Default to 4-bit if not found


def create_output_path(model_input_path, q_type):
    output_path = os.path.dirname(model_input_path)
    model_name = os.path.basename(output_path)
    os.makedirs(output_path, exist_ok=True)
    output_model = f"{model_name}.GGMLv3.{q_type}.bin"
    return os.path.join(output_path, output_model)


@click.command()
@click.argument(
    "model_input_path",
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True,
    ),
)
@click.option(
    "--model_output_path",
    type=click.Path(
        exists=False,
        writable=True,
    ),
    default=None,
    help="Path to store the quantized model. If not provided, a standard path will be used.",
)
@click.option(
    "--q_type",
    type=click.Choice(QUANTIZATION_TYPE_KEYS),
    default="q4_0",
    help="The type of quantization to apply to the model. Quantization reduces the model size by representing weights in lower bit widths. Default is 'q4_0'.",
)
def main(model_input_path, model_output_path, q_type):
    # Ensure converted model exists
    if not os.path.exists(model_input_path):
        raise RuntimeError(f"Converted model does not exist ({model_input_path})")

    logging.info(f"Using Input Path: {model_input_path}")
    fname_inp = model_input_path.encode("utf-8")

    # Construct the models output file path
    if model_output_path is None:
        fname_out = create_output_path(model_input_path, q_type)
    else:
        fname_out = model_output_path

    if os.path.exists(fname_out):
        raise RuntimeError(f"Quantized model already exists ({fname_out})")

    # Encode output file path to bytes
    logging.info(f"Using Output Path: {fname_out}")
    fname_out = fname_out.encode("utf-8")

    # Get the default C struct parameters
    logging.info("Initializing Quantization Parameters")
    params = llama_model_quantize_default_params()

    # Set the quantization type
    # Defaults to 4-bit if not found
    logging.info(f"Using Quantization Type: {q_type}")
    # enum llama_ftype ftype; // quantize to this llama_ftype
    params.ftype = get_quantization_type(q_type)

    # Set the number of threads
    params.nthread = os.cpu_count() or 2
    logging.info(f"Using CPU Count: {params.nthread}")
    # You can also set other fields as needed

    logging.info("Starting Quantization Process...")
    return_code = llama_model_quantize(fname_inp, fname_out, params)

    if return_code == 0:
        logging.info(f"Quantized model saved to {fname_out}")
    else:
        logging.error(f"Quantization failed with code: {return_code}")


if __name__ == "__main__":
    main()
