"""
gguf_chat_template.py - example file to extract the chat template from the models metadata
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import jinja2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_vendor_gguf_path():
    root_dir = Path(__file__).resolve().parent.parent.parent
    gguf_py_dir = root_dir / "vendor/llama.cpp/gguf-py"
    logger.info(f"Using Vendor Release: {gguf_py_dir}")
    return str(gguf_py_dir)


try:
    import gguf

    logger.info("GGUF: Successfully imported GGUF.")
except ImportError:
    logger.warning("GGUF is not installed. Attempting to fallback to vendor release.")
    gguf_py_dir = get_vendor_gguf_path()

    # Insert the path for import availability
    sys.path.insert(1, gguf_py_dir)

    try:
        import gguf

        logger.info("GGUF: Successfully referring to vendor release")
    except ImportError:
        logger.error("GGUF: Package not found in vendor release.")


def get_chat_template(model_file: str) -> str:
    reader = gguf.GGUFReader(model_file)

    # Available keys
    logger.info("Detected model metadata!")
    logger.info("Outputting available model fields:")
    for key in reader.fields.keys():
        logger.info(key)

    # Access the 'chat_template' field directly using its key
    chat_template_field = reader.fields.get(gguf.Keys.Tokenizer.CHAT_TEMPLATE)

    if chat_template_field:
        # Extract the chat template string from the field
        chat_template_memmap = chat_template_field.parts[-1]
        chat_template_string = chat_template_memmap.tobytes().decode("utf-8")
        return chat_template_string
    else:
        logger.error("Chat template field not found in model metadata.")
        return ""


def display_chat_template(chat_template: str, format_template: bool = False):
    """
    Display the chat template to standard output, optionally formatting it using Jinja2.

    Args:
        chat_template (str): The extracted chat template.
        format_template (bool, optional): Whether to format the template using Jinja2. Defaults to False.
    """
    logger.info(f"Format Template: {format_template}")

    if format_template:
        # Render the formatted template using Jinja2 with a context that includes 'bos_token' and 'eos_token'
        env = jinja2.Environment(
            loader=jinja2.BaseLoader(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.from_string(chat_template)
        formatted_template = template.render(
            messages=[
                {"role": "system", "content": "I am a helpful assistant."},
                {"role": "user", "content": "Hello!"},
            ],
            bos_token="[BOS]",
            eos_token="[EOS]",
        )
        print(formatted_template)
    else:
        # Display the raw template
        print(chat_template)


# Example usage:
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract chat template from a GGUF model file"
    )
    parser.add_argument("model_file", type=str, help="Path to the GGUF model file")
    parser.add_argument(
        "--format",
        action="store_true",
        help="Format the chat template using Jinja2",
    )

    args = parser.parse_args()

    model_file = args.model_file
    chat_template = get_chat_template(model_file)

    display_chat_template(chat_template, format_template=args.format)


if __name__ == "__main__":
    main()
