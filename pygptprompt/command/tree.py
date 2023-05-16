import os
from typing import List, Optional


def tree(
    path: str,
    prefix: str = "",
    _results: Optional[List[str]] = None,
    ignore_dirs: Optional[List[str]] = None,
) -> List[str]:
    if _results is None:
        _results = []

    if ignore_dirs is None:
        ignore_dirs = []

    for entry in os.scandir(path):
        entry_path = os.path.join(path, entry.name)

        if entry.is_file():
            _results.append(f"{prefix}├── {entry.name}")
        elif entry.is_dir():
            if entry.name not in ignore_dirs:
                _results.append(f"{prefix}└── {entry.name}")
                _new_prefix = prefix + "    "
                tree(entry_path, _new_prefix, _results, ignore_dirs)

    return _results


def display_tree(command: str) -> str:
    args = command.split()

    # Validation
    if len(args) < 2:
        return "Usage: /tree <directory> [--ignore dir1,dir2,...]"

    directory = args[1]
    ignore_dirs = []

    if "--ignore" in args:
        try:
            ignore_index = args.index("--ignore")
            ignore_value = args[ignore_index + 1]
            ignore_dirs = ignore_value.split(",")
        except (IndexError, ValueError):
            return "Error: Invalid format for --ignore option."

    # Check if the directory exists and is a directory
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return f"Error: {directory} is not a valid directory."

    # Generate the tree
    tree_lines = tree(directory, ignore_dirs=ignore_dirs)

    # Combine the lines into a single string
    return "\n".join(tree_lines)
