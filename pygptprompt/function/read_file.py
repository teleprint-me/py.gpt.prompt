def read_file_in_chunks(
    filepath: str,
    start_line: int,
    end_line: int = None,
) -> str:
    """
    Reads a portion of a file from start_line to end_line.

    :param filepath: Path of the file to read.
    :param start_line: The line number to start reading from.
    :param end_line: The line number to stop reading at. Reads till the end if None.
    :return: The extracted content of the file.
    """
    with open(filepath, "r") as file:
        # Skip lines until the start line is reached
        for _ in range(start_line):
            next(file)

        # Read and store lines until the end line is reached or the file ends
        lines = []
        for i, line in enumerate(file, start=1):
            if end_line is not None and i > end_line - start_line:
                break
            lines.append(line)

    return "".join(lines)


# Example usage:
# content = read_file_in_chunks('path/to/your/file.py', 100, 200)
# This reads lines 100 to 200 of the file
