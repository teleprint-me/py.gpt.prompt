import os

import click
from llama_cpp import (
    LLAMA_FTYPE_MOSTLY_F16,
    LLAMA_FTYPE_MOSTLY_Q4_0,
    LLAMA_FTYPE_MOSTLY_Q5_0,
    LLAMA_FTYPE_MOSTLY_Q8_0,
    llama_model_quantize,
)

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


@click.command()
@click.argument("model_input_path", type=click.Path(exists=True))
@click.argument("model_output_path", type=click.Path(exists=False))
@click.option(
    "--quantization_type",
    type=click.Choice(list(QUANTIZATION_TYPE_KEYS)),
    default="q4_0",
    help="The number of bits to use for quantization.",
)
def main(model_input_path, model_output_path, quantization_type):
    if os.path.exists(model_output_path):
        raise RuntimeError(f"Quantized model already exists ({model_output_path})")
    qtype = get_quantization_type(quantization_type)
    return_code = llama_model_quantize(
        model_input_path.encode("utf-8"),
        model_output_path.encode("utf-8"),
        qtype,  # enum llama_ftype ftype; // quantize to this llama_ftype
    )
    if return_code != 0:
        raise RuntimeError("Failed to quantize model")


if __name__ == "__main__":
    main()
