# pygptprompt/database/__init__.py
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

This module contains the initialization code and configuration
settings for the package.

Constants:
- ROOT_DIRECTORY: The absolute path of the current working directory.
- SOURCE_DIRECTORY: The folder path for storing the source documents.
- PERSIST_DIRECTORY: The folder path for storing the database.
- INGEST_THREADS: The number of CPU threads for ingestion.
- CHROMA_SETTINGS: The settings object for the Chroma database.
- MIME_TYPES: A mapping of MIME types to loader classes.
- LANGUAGE_TYPES: A mapping of file extensions to the Language enumeration.
- EMBEDDING_TYPES: A mapping of embedding type names to embedding classes.
- DEFAULT_DEVICE_TYPE: The default device type for embeddings.
- DEFAULT_EMBEDDING_MODEL: The default embedding model.
- DEFAULT_EMBEDDING_TYPE: The default embedding type.
- DEFAULT_MODEL_REPOSITORY: The default model git repository.
- DEFAULT_MODEL_SAFETENSORS: The default model weights base name.

Classes:
- Language: An enumeration representing programming language types.

Note: The default paths for SOURCE_DIRECTORY and PERSIST_DIRECTORY are 
set based on the package structure and can be customized if needed.
"""

import logging
import os
from typing import List, Tuple, Type

from chromadb.config import Settings
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

# Get the path for this source file
SOURCE_PATH: str = os.path.dirname(os.path.realpath(__file__))
# Get the absolute path of the package root directory
ROOT_DIRECTORY: str = os.path.abspath(os.path.join(SOURCE_PATH, ".."))
# Set the default path for storing the source documents
SOURCE_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "SOURCE_DOCUMENTS")
# Set the default path for storing the database
PERSIST_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "DB")

# The number of CPU threads for ingestion
# If os.cpu_count() is not available, it defaults to 8
INGEST_THREADS: int = os.cpu_count() or 8

# NOTE: IMPORTANT: MODEL_REPOSITORY
# Models are downloaded at runtime.
# The label convention is <username>/<repository>
# where <username>/<repository> represents the url endpoint
# e.g.
#   ~/.cache/huggingface/hub
#   ~/.cache/torch/sentence_transformers

# The default device type to compute with
DEFAULT_DEVICE_TYPE: str = "cpu"
# The default embedding model
DEFAULT_EMBEDDING_MODEL: str = "hkunlp/instructor-large"
# The default embedding type
DEFAULT_EMBEDDING_TYPE: str = "HuggingFaceInstructEmbeddings"
# The default model git repository
DEFAULT_MODEL_REPOSITORY: str = "TheBloke/orca_mini_7B-GGML"

# A mapping of MIME types to loader classes
MIME_TYPES: Tuple[Tuple[str, Type[BaseLoader]], ...] = (
    ("text/plain", TextLoader),
    ("application/pdf", PDFMinerLoader),
    ("text/csv", CSVLoader),
    ("application/vnd.ms-excel", UnstructuredExcelLoader),
)

# A mapping of file extensions to the Language enumeration
LANGUAGE_TYPES: Tuple[Tuple[str, str], ...] = (
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

# A mapping of embedding type names to embedding classes
EMBEDDING_TYPES: dict[str, Type[Embeddings]] = {
    "HuggingFaceInstructEmbeddings": HuggingFaceInstructEmbeddings,
    "HuggingFaceEmbeddings": HuggingFaceEmbeddings,
    "SentenceTransformerEmbeddings": SentenceTransformerEmbeddings,
    "OpenAIEmbeddings": OpenAIEmbeddings,
}

CHOICE_EMBEDDING_TYPES: List[str] = [
    "HuggingFaceEmbeddings",
    "HuggingFaceInstructEmbeddings",
]

CHOICE_EMBEDDING_MODELS: List[str] = [
    "hkunlp/instructor-base",
    "hkunlp/instructor-large",
    "hkunlp/instructor-xl",
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-MiniLM-L12-v2",
]

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

CHOICE_DEVICE_TYPES: list[str] = [
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
