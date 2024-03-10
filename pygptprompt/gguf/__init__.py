import os
from importlib import import_module

from .constants import *
from .gguf_reader import *
from .gguf_writer import *
from .tensor_mapping import *
from .vocab import *

os.environ["NO_LOCAL_GGUF"] = "TRUE"

gguf_convert_endian_entrypoint = import_module("scripts.gguf-convert-endian").main
gguf_dump_entrypoint = import_module("scripts.gguf-dump").main
gguf_set_metadata_entrypoint = import_module("scripts.gguf-set-metadata").main

del import_module, os
