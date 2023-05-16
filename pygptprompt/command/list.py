import os


def get_file_info(file_path: str) -> str:
    is_dir = os.path.isdir(file_path)
    if is_dir:
        file_size = "-"
    else:
        file_size = os.path.getsize(file_path)

    type_info = "dir" if is_dir else "file"
    return f"{file_path:30} {type_info:10} {file_size}"


def list_directory(command: str) -> str:
    directory = command.replace("/ls", "").strip()

    if not os.path.isdir(directory):
        return f"Error: Directory {directory} not found."

    try:
        files = os.listdir(directory)
        file_info_list = [
            get_file_info(os.path.join(directory, file)) for file in files
        ]
        return "\n".join(file_info_list)
    except Exception as e:
        return f"Error listing directory {directory}: {str(e)}."
