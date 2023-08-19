"""
pygptprompt/quantize.py

NOTE:
    GGML Quantization is being deprecated in favor of GGUF Quantization.
    This is just a prototype to experiment with.
"""
import os

import click
from llama_cpp import (
    LLAMA_FTYPE_MOSTLY_F16,
    LLAMA_FTYPE_MOSTLY_Q4_0,
    LLAMA_FTYPE_MOSTLY_Q5_0,
    LLAMA_FTYPE_MOSTLY_Q8_0,
    llama_model_quantize,
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


def create_output_path(input_path, q_type):
    model_name = os.path.basename(input_path)
    output_path = os.path.join(os.getcwd(), "GGML", model_name)
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
    type=click.Path(exists=False),
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
    if model_output_path is None:
        output_path = create_output_path(model_input_path, q_type)
    else:
        output_path = model_output_path

    if os.path.exists(output_path):
        raise RuntimeError(f"Quantized model already exists ({output_path})")

    f_type = get_quantization_type(q_type)

    return_code = llama_model_quantize(
        model_input_path.encode("utf-8"),
        output_path.encode("utf-8"),
        f_type,  # enum llama_ftype ftype; // quantize to this llama_ftype
    )

    if return_code != 0:
        raise RuntimeError("Failed to quantize model")


if __name__ == "__main__":
    main()
