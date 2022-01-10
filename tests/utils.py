from pathlib import Path


def write_something_to_file(tmp_file_path: Path, content: str):
    with open(tmp_file_path, "w") as file:
        file.write(content)
