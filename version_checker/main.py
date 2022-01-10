import argparse
import typing
from pathlib import Path


def version_in_file(version: str, file_path: typing.Union[str, Path]) -> bool:
    with open(file_path, "r") as file:
        content = file.read()
    return version in content


def main(argv: typing.Optional[typing.List[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="version that files must have")
    parser.add_argument(
        "--files", nargs="*", help="files in which the version will be checked"
    )
    args = parser.parse_args(argv)
    return (
        0
        if all(version_in_file(args.version, file) for file in args.files)
        else 1
    )
