"""
gguf_metadata.py - example file to extract metadata from a language model
"""

import argparse
import ctypes
import logging
from pathlib import Path

from llama_cpp import llama, llama_cpp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retrieve_metadata(llama_model, key="general.architecture", verbose=False):
    """
    Retrieve metadata from a LLaMA model.

    Args:
        model_path (str): Path to the LLaMA model file.
        key (str, optional): The metadata key to retrieve. Defaults to "general.architecture".
        verbose (bool, optional): Whether to display verbose output. Defaults to False.

    Returns:
        str: The retrieved metadata value or "Metadata key not found" if the key is not found.
    """
    buflen = 2048  # number of bytes for memory allocation
    buf = (ctypes.c_char * buflen)(0)  # allocate memory to pointer

    # // Get metadata value as a string by key name
    # LLAMA_API int llama_model_meta_val_str(
    #   const struct llama_model * model,
    #   const char * key,
    #   char * buf,
    #   size_t buf_size);
    metadata = llama_cpp.llama_model_meta_val_str(
        llama_model.model, key.encode(), buf, ctypes.sizeof(buf)
    )

    if metadata >= 0:
        value = buf.value.decode()
    else:
        value = "Metadata key not found"

    return value


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve metadata from a LLaMA model."
    )
    parser.add_argument("model_path", type=str, help="Path to the LLaMA model file.")
    parser.add_argument(
        "--key",
        type=str,
        default="general.architecture",
        help="Metadata key to retrieve (default: 'general.architecture').",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    args = parser.parse_args()

    # FIXME: pathlib.Path is not compatible with the Llama class
    # We still need it to simplify getting the model file name from the path.
    model_path = Path(args.model_path)
    key = args.key
    verbose = args.verbose

    logger.info(f"Loading model: {model_path.parts[-1]}")
    llama_model = llama.Llama(str(model_path), verbose=verbose)
    logger.info(f"Successfully loaded {model_path.parts[-1]}.")

    logger.info(f"Attempting to extract '{key}' from {model_path.parts[-1]}.")
    value = retrieve_metadata(llama_model, key, verbose)
    logging.info(f"Extracted Metadata: {key}: {value}")


if __name__ == "__main__":
    main()
