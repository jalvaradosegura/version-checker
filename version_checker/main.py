import argparse
import typing
from pathlib import Path


def get_version_from_toml(toml_file_path: typing.Union[Path]) -> str:
    with open(toml_file_path, "r") as toml_file:
        for line in toml_file.readlines():
            if line.startswith("version = "):
                version = line.split("=")[1].strip().replace('"', "")
                return version
        raise ValueError(
            "Couldn't find package version within the .toml file.\n"
            "Try giving a value to the --version parameter."
        )


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

    if args.version is None:
        args.version = get_version_from_toml("pyproject.toml")

    return (
        0
        if all(version_in_file(args.version, file) for file in args.files)
        else 1
    )
