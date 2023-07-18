import os


def evaluate_path(path: str) -> str:
    """
    Evaluate a path, expanding ~ and environment variables.

    Args:
        path (str): The path to evaluate.

    Returns:
        str: The evaluated path.
    """
    return os.path.expanduser(os.path.expandvars(path))
