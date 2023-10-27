import os
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, Generic, List, Protocol, Type, TypeVar, Union

import inquirer
import safetensors
import torch

TModelFile = TypeVar("TModelFile")
TTensor = TypeVar("TTensor")


class ReaderException(Exception):
    pass


class Reader(Protocol):
    def __init__(self, path: Union[str, Path]):
        self.path = path

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value: Union[str, Path]) -> None:
        if isinstance(value, str):
            value = Path(value)
        if not isinstance(value, Path):
            raise ValueError("Invalid path type. Expected str or pathlib.Path.")
        if not value.is_dir():
            raise ReaderException("Expected a directory and got a file instead.")
        self._path = value


class TensorReader(Reader, Generic[TModelFile, TTensor]):
    def __init__(self, path: Union[str, Path], suffixes: set[str]):
        super().__init__(path)

        self.files = self._select_model_files(suffixes)
        self.models = self._load_model_files()
        self.tensors = self._load_model_tensors()

    def _select_model_files(self, suffixes: set[str]) -> List[Path]:
        models = []

        for file in os.scandir(self.path):
            path = Path(file.path)
            suffix = path.suffix

            if suffix in suffixes:
                models.append(path)

        if not models:
            raise ReaderException(
                "No model-related files found in the given directory."
            )

        questions = [
            inquirer.Checkbox(
                "selected_files",
                message="Select model files",
                choices=models,
            ),
        ]

        answers = inquirer.prompt(questions)
        selected_files = answers.get("selected_files", [])

        return selected_files

    def _load_model_files(self) -> List[TModelFile]:
        ...

    def _load_model_tensors(self) -> Dict[str, TTensor]:
        ...

    def dump_files_to_stdout(self):
        for file in self.files:
            print(f"File: {file}, Size: {file.stat().st_size} bytes")

    def dump_tensor_to_stdout(self, tensor_name: str):
        try:
            tensor = self.tensors[tensor_name]
            print(f"Tensor Name: {tensor_name}")
            print(f"Data Type: {tensor.dtype}")
            print(f"Dimensions: {tensor.dim()}")
            print(f"Shape: {tensor.shape}")
            print(f"Element count: {tensor.numel()}")
        except KeyError:
            print(f"Tensor '{tensor_name}' not found.")

    def dump_all_tensors_to_stdout(self):
        if not self.tensors:
            print("No tensors found in the model directory.")
            return

        for name, tensor in self.tensors.items():
            print(f"---- Tensor {name} ----")
            print(f"Data Type: {tensor.dtype}")
            print(f"Dimensions: {tensor.dim()}")
            print(f"Shape: {tensor.shape}")
            print(f"Element count: {tensor.numel()}")
            print("------------------------")

    def dump_all_tensor_names_to_stdout(self):
        for name, tensor in self.tensors.items():
            print(name)


class TorchReader(TensorReader[Dict[str, torch.Tensor], torch.Tensor]):
    def __init__(self, path: Union[str, Path]):
        super().__init__(path, suffixes={".pt", ".pth", ".bin"})

    def _load_model_files(self) -> List[Dict[str, torch.Tensor]]:
        return [torch.load(path) for path in self.files]

    def _load_model_tensors(self) -> Dict[str, torch.Tensor]:
        model = {}
        for shard in self.models:
            model |= shard
        return model


class SafeTensorReader(TensorReader[safetensors.safe_open, torch.Tensor]):
    def __init__(self, path: Union[str, Path]):
        super().__init__(path, suffixes={".safetensors"})

    def _load_model_files(self) -> List[safetensors.safe_open]:
        return [safetensors.safe_open(path, framework="torch") for path in self.files]

    def _load_model_tensors(self) -> Dict[str, torch.Tensor]:
        tensors = {}
        for model in self.models:
            for key in model.keys():
                tensors[key] = model.get_tensor(key)
        return tensors


class ReaderFactory(Reader):
    def __init__(self, path: Union[str, Path]):
        super().__init__(path)

    def identify_file_types(self) -> set[str]:
        tensor_types = set()
        for p in self.path.iterdir():
            if p.suffix in {".safetensors"}:
                tensor_types.add("safetensor")
            elif p.suffix in {".pt", ".pth", ".bin"}:
                tensor_types.add("torch")
        if not tensor_types:
            raise ValueError("Unknown model type. Cowardly refusing to continue.")
        return tensor_types

    def select_file_type(self, tensor_types: set[str]) -> str:
        # If more than one type found, ask the user
        if len(tensor_types) > 1:
            questions = [
                inquirer.List(
                    "reader",
                    message="Which tensor type would you like to read?",
                    choices=list(tensor_types),
                ),
            ]
            answers = inquirer.prompt(questions)
            return answers["reader"]
        elif len(tensor_types) == 1:
            return next(iter(tensor_types))
        else:
            raise ValueError("No recognized tensor files found.")

    def select_reader(self, selected_type: str) -> Type[TensorReader]:
        if selected_type == "safetensor":
            return SafeTensorReader
        elif selected_type == "torch":
            return TorchReader
        else:
            raise ReaderException("Unknown tensor type.")


def get_arguments() -> Namespace:
    parser = ArgumentParser(
        description="Dump tensor data for a model within a directory"
    )
    parser.add_argument("path", help="Path to the model directory")
    parser.add_argument(
        "-f", "--files", action="store_true", help="View files and their sizes"
    )
    parser.add_argument(
        "-t",
        "--tensor",
        metavar="TENSOR_NAME",
        help="View a specific tensor in standard output",
    )
    parser.add_argument(
        "-a",
        "--all-tensors",
        action="store_true",
        help="View all tensors in standard output",
    )
    parser.add_argument(
        "-n",
        "--all-tensor-names",
        action="store_true",
        help="View all tensor names in standard output",
    )
    return parser.parse_args()


def main(args):
    # Create the reader factory
    reader_factory = ReaderFactory(args.path)
    # Scan directory to identify file types
    tensor_types = reader_factory.identify_file_types()
    # If more than one file type is found, ask the user
    selected_type = reader_factory.select_file_type(tensor_types)
    # Return the reader class based on auto-detection or the user's choice
    ReaderClass = reader_factory.select_reader(selected_type)
    # Instantiate the tensor reader
    reader = ReaderClass(args.path)

    if args.tensor:
        reader.dump_tensor_to_stdout(args.tensor)
    elif args.all_tensors:
        reader.dump_all_tensors_to_stdout()
    elif args.all_tensor_names:
        reader.dump_all_tensor_names_to_stdout()
    else:
        reader.dump_files_to_stdout()


if __name__ == "__main__":
    main(get_arguments())
