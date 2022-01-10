import typing
from pathlib import Path


def version_in_file(version: str, file_path: typing.Union[str, Path]) -> bool:
    with open(file_path, "r") as file:
        content = file.read()
    return version in content
