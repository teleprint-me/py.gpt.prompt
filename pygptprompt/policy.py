import os


def is_accessible(
    path: str,
    allowed_paths: list[str],
    denied_paths: list[str],
) -> bool:
    path = os.path.abspath(path)
    for denied_path in denied_paths:
        if path.startswith(os.path.abspath(denied_path)):
            return False
    for allowed_path in allowed_paths:
        if path.startswith(os.path.abspath(allowed_path)):
            return True
    return False
