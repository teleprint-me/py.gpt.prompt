"""
"There is a stubbornness about me that never can bear to be frightened at the will of others. My courage always rises at every attempt to intimidate me."
  - Jane Austen, Pride and Prejudice

pygptprompt/__init__.py

NOTE:

Models can be manually downloaded before runtime.

Models can be optionally downloaded at runtime.

The context window size may vary from model to model and can
be easily adjusted as required.

NOTE: IMPORTANT: MODEL_REPOSITORY

Model reference:

  <username>/<repository>

  - where <username>/<repository> represents the url endpoint

  - where `hf_hub_download` writes [source] to [destination].

For example:
  ~/.cache/huggingface/hub/models--TheBloke--orca_mini_7B-GGML

NOTE: IMPORTANT: MODEL_FILENAME

Identifier reference:

  <model-id>.<n-params>.<ggml-version>.<quant-type>.<extension>

  - where <model-id> represents the specific model identifier.

For example:
  orca-mini-7b.ggmlv3.q2_K.bin
"""
import os

__version__ = "0.0.30"

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

# NOTE:
# This is here for future reference.
# This will be removed once obsoleted.
#
# from pygptprompt.processor.image import ImageProcessor
# from pygptprompt.processor.pdf import PDFProcessor
#
# # A mapping of MIME types to langchain loader classes
# MAP_MIME_TYPES: tuple[tuple[str, type[object]], ...] = (
#     # ("text/plain", TextProcessor),
#     # ("text/csv", CSVProcessor),
#     ("application/pdf", PDFProcessor),
#     ("image/png", ImageProcessor),
#     ("image/jpeg", ImageProcessor),
# )
