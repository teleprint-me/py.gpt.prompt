import os

import click
import llama_cpp

# Mapping between user-friendly quantization type and the expected integer value
QUANTIZATION_TYPE_MAPPING = {
    "f32": 0,
    "f16": 1,
    "q4_1": 2,
    "q4_0": 3,
}


@click.command()
@click.argument("model_input_path", type=click.Path(exists=True))
@click.argument("model_output_path", type=click.Path(exists=False))
@click.option(
    "--quantization_type",
    type=click.Choice(list(QUANTIZATION_TYPE_MAPPING.keys())),
    default="q4_0",
    help="The number of bits to use for quantization.",
)
def main(model_input_path, model_output_path, quantization_type):
    if os.path.exists(model_output_path):
        raise RuntimeError(f"Quantized model already exists ({model_output_path})")
    qtype = QUANTIZATION_TYPE_MAPPING.get(quantization_type, 3)  # default to q4_0
    return_code = llama_cpp.llama_model_quantize(
        model_input_path.encode("utf-8"), model_output_path.encode("utf-8"), qtype
    )
    if return_code != 0:
        raise RuntimeError("Failed to quantize model")


if __name__ == "__main__":
    main()
