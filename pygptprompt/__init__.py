# pygptprompt/__init__.py
#
# Copyright 2023 PromtEngineer/localGPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
"No plan survives contact with the enemy."
    - Helmuth von Moltke

Initialization code and configuration settings for the PyGPTPrompt package.

Constants:
- PATH_HOME: The user's home path.
- PATH_CACHE: The default cache path for PyGPTPrompt.
- PATH_CONFIG: The default config path for PyGPTPrompt.
- PATH_LOCAL: The default local path for PyGPTPrompt.
- PATH_SOURCE: The default path for storing source documents.
- PATH_DATABASE: The default path for storing the database.
- DEFAULT_DEVICE_TYPE: The default device type for embeddings.
- DEFAULT_CPU_COUNT: The default number of CPU threads for ingestion.
- DEFAULT_N_CTX: The default context window size for llama.cpp Model.
- DEFAULT_MAX_TOKENS: The default maximum number of tokens for llama.cpp Model.
- DEFAULT_TEMPERATURE: The default temperature for llama.cpp Model.
- DEFAULT_TOP_P: The default top-p value for llama.cpp Model.
- DEFAULT_N_GPU_LAYERS: The default number of GPU layers for llama.cpp GPU settings.
- DEFAULT_N_BATCH: The default batch size for llama.cpp GPU settings.
- DEFAULT_LOW_VRAM: The default low VRAM flag for llama.cpp GPU settings.
- DEFAULT_EMBEDDINGS_MODEL: The default embeddings model.
- DEFAULT_EMBEDDINGS_CLASS: The default embeddings class definition.
- DEFAULT_MODEL_REPOSITORY: The default model git repository.
- DEFAULT_MODEL_FILENAME: The default ggml model filename.

Classes:
- Language: An enumeration representing programming language types.

Note: The default paths for SOURCE_DIRECTORY and PERSIST_DIRECTORY are set based
on the package structure and can be customized if needed.
"""

import logging
import os
from pathlib import Path
from typing import List, Tuple, Type, Union

from langchain.document_loaders import (
    CSVLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredExcelLoader,
)
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import (
    HuggingFaceEmbeddings,
    HuggingFaceInstructEmbeddings,
    OpenAIEmbeddings,
    SentenceTransformerEmbeddings,
)
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import Language

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

# The default device type to compute with
DEFAULT_DEVICE_TYPE: str = "cpu"

# The number of CPU threads for ingestion
# Use os.sched_getaffinity(0) to get the set of CPUs the current process can run on
# If the count cannot be determined, assume duo-core CPU availability as a fallback
DEFAULT_CPU_COUNT: int = len(os.sched_getaffinity(0)) or 2

# The default llama.cpp Model settings
# NOTE: Llama models usually have a maximum token limit of 2048.
# The context window size may vary from model to model and can
# be easily adjusted as required.
DEFAULT_N_CTX: int = 2048
DEFAULT_MAX_TOKENS: int = 512
DEFAULT_TEMPERATURE: float = 0.8
DEFAULT_TOP_P: float = 0.95

# The default llama.cpp GPU settings
DEFAULT_N_GPU_LAYERS: int = 0
DEFAULT_N_BATCH: int = 512
DEFAULT_LOW_VRAM: bool = False

# The default embedding model
DEFAULT_EMBEDDINGS_MODEL: str = "hkunlp/instructor-large"

# The default embedding type
DEFAULT_EMBEDDINGS_CLASS: str = "HuggingFaceInstructEmbeddings"

# NOTE: IMPORTANT: MODEL_REPOSITORY
# Models are downloaded at runtime.
# The label convention is <username>/<repository>
# where <username>/<repository> represents the url endpoint
# where `hf_hub_download` writes [source] to [destination].
# For example:
#   ~/.cache/huggingface/hub/models--TheBloke--orca_mini_7B-GGML

# The default model git repository
DEFAULT_MODEL_REPOSITORY: str = "TheBloke/orca_mini_7B-GGML"

# The default ggml model filename from the given git repository
# NOTE: IMPORTANT: MODEL_FILENAME
# Models are downloaded at runtime.
# The identifier convention is
# <model-id>.<n-params>.<ggml-version>.<quant-type>.<extension>
# where <model-id> represents the specific model identifier.
# For example:
#   orca-mini-7b.ggmlv3.q2_K.bin
# The filename follows the convention for the downloaded model files.

DEFAULT_MODEL_FILENAME: str = "orca-mini-7b.ggmlv3.q5_1.bin"

# A mapping of MIME types to loader classes
MAP_MIME_TYPES: Tuple[Tuple[str, Type[BaseLoader]], ...] = (
    ("text/plain", TextLoader),
    ("application/pdf", PDFMinerLoader),
    ("text/csv", CSVLoader),
    ("application/vnd.ms-excel", UnstructuredExcelLoader),
)

# A mapping of file extensions to the Language enumeration
MAP_LANGUAGE_ENUM: Tuple[Tuple[str, str], ...] = (
    ("cpp", Language.CPP),  # C++ source files
    ("go", Language.GO),  # Go source files
    ("java", Language.JAVA),  # Java source files
    ("js", Language.JS),  # JavaScript source files
    ("php", Language.PHP),  # PHP source files
    ("proto", Language.PROTO),  # Protocol Buffers files
    ("py", Language.PYTHON),  # Python source files
    ("rst", Language.RST),  # reStructuredText files
    ("rb", Language.RUBY),  # Ruby source files
    ("rs", Language.RUST),  # Rust source files
    ("scala", Language.SCALA),  # Scala source files
    ("swift", Language.SWIFT),  # Swift source files
    ("md", Language.MARKDOWN),  # Markdown files
    ("tex", Language.LATEX),  # LaTeX files
    ("html", Language.HTML),  # HTML files
    ("sol", Language.SOL),  # Solidity files
)

# A mapping of embeddings identifiers to classes
MAP_EMBEDDINGS_CLASS: dict[str, Type[Embeddings]] = {
    "HuggingFaceInstructEmbeddings": HuggingFaceInstructEmbeddings,
    "HuggingFaceEmbeddings": HuggingFaceEmbeddings,
    "SentenceTransformerEmbeddings": SentenceTransformerEmbeddings,
    "OpenAIEmbeddings": OpenAIEmbeddings,
}

# A List of supported embeddings class definitions
CHOICE_EMBEDDING_TYPES: List[str] = [
    "HuggingFaceEmbeddings",
    "HuggingFaceInstructEmbeddings",
]

# A List of supported embeddings instruct models
CHOICE_EMBEDDING_MODELS: List[str] = [
    "hkunlp/instructor-base",
    "hkunlp/instructor-large",
    "hkunlp/instructor-xl",
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-MiniLM-L12-v2",
]

# A List of recommended instruct models
CHOICE_MODEL_REPOSITORIES: List[str] = [
    # 3B GGML Models
    "TheBloke/orca_mini_3B-GGML",
    # 7B GGML Models
    "TheBloke/orca_mini_7B-GGML",
    "TheBloke/falcon-7b-instruct-GGML",
    "TheBloke/wizardLM-7B-GGML",
    "TheBloke/WizardLM-Uncensored-Falcon-7B-GGML",
    # 13B GGML Models
    "TheBloke/orca_mini_13B-GGML",
]

# A List of PyTorch supported device types
CHOICE_DEVICE_TYPES: List[str] = [
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
