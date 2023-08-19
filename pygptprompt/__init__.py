"""
"There is a stubbornness about me that never can bear to be frightened at the will of others. My courage always rises at every attempt to intimidate me."
  - Jane Austen, Pride and Prejudice

pygptprompt/__init__.py

Initialization code and configuration settings for the PyGPTPrompt package.

NOTE: Llama models usually have a maximum token limit of 2048.
The context window size may vary from model to model and can
be easily adjusted as required.

NOTE: IMPORTANT: MODEL_REPOSITORY
Models are downloaded at runtime.
The label convention is <username>/<repository>
where <username>/<repository> represents the url endpoint
where `hf_hub_download` writes [source] to [destination].
For example:
  ~/.cache/huggingface/hub/models--TheBloke--orca_mini_7B-GGML

NOTE: IMPORTANT: MODEL_FILENAME
Models are downloaded at runtime.
The identifier convention is
<model-id>.<n-params>.<ggml-version>.<quant-type>.<extension>
where <model-id> represents the specific model identifier.
For example:
  orca-mini-7b.ggmlv3.q2_K.bin
The filename follows the convention for the downloaded model files.
"""

import logging
import os
from pathlib import Path
from typing import List, Union

# from pygptprompt.processor.image import ImageProcessor
# from pygptprompt.processor.pdf import PDFProcessor

__version__ = "0.0.20"

# Set logging configuration
# NOTE: Can be overridden on a script-by-script basis
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.INFO,
)

# Get the user's home path
PATH_HOME: Union[str, Path] = Path.home()
# Set the default cache path
PATH_CACHE: Union[str, Path] = Path(PATH_HOME, ".cache", "pygptprompt")
# Set the default config path
PATH_CONFIG: Union[str, Path] = Path(PATH_HOME, ".config", "pygptprompt")
# Set the default local path
PATH_LOCAL: Union[str, Path] = Path(PATH_HOME, ".local", "share", "pygptprompt")
# Set the default path for storing the source documents
PATH_SOURCE: Union[str, Path] = Path(PATH_CACHE, "source")
# Set the default path for storing the database
PATH_DATABASE: Union[str, Path] = Path(PATH_CACHE, "database")

# The number of CPU threads for ingestion
# Use os.sched_getaffinity(0) to get the set of threads
# the current process can be prioritized by.
# If the set of threads cannot be determined,
# get the CPU core count or assume duo-core CPU availability
# as a fallback.
try:
    CPU_COUNT: int = len(os.sched_getaffinity(0))
except AttributeError:
    CPU_COUNT: int = os.cpu_count() or 2

# The default system message for the employed model
SYSTEM_MESSAGE = {
    "role": "system",
    "content": "My name is GPT. I am a helpful programming assistant.",
}

# A List of PyTorch supported device types
TORCH_DEVICE_TYPES: List[str] = [
    "cpu",
    "cuda",
    "ipu",
    "xpu",
    "mkldnn",
    "opengl",
    "opencl",
    "ideep",
    "hip",
    "ve",
    "fpga",
    "ort",
    "xla",
    "lazy",
    "vulkan",
    "mps",
    "meta",
    "hpu",
    "mtia",
]

# # A mapping of MIME types to langchain loader classes
# MAP_MIME_TYPES: tuple[tuple[str, type[object]], ...] = (
#     # ("text/plain", TextProcessor),
#     # ("text/csv", CSVProcessor),
#     ("application/pdf", PDFProcessor),
#     ("image/png", ImageProcessor),
#     ("image/jpeg", ImageProcessor),
# )
