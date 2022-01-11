import argparse
import typing
from importlib.metadata import version
from pathlib import Path

from loguru import logger


def check_files(
    files_path: typing.List[typing.Union[str, Path]], version: str
) -> bool:
    files_status = []
    for index, file in enumerate(files_path):
        logger.info(f"checking {index + 1}/{len(files_path)}: {file}...")
        status = version_in_file(version, file)
        files_status.append(status)
        if status:
            logger.success(f"{file} contains version: {version} ✅")
        else:
            logger.error(f"{file} doesn't contain version: {version} ❌")

    return all(files_status)


def get_version_from_toml(toml_file_path: typing.Union[Path]) -> str:
    logger.info(f"grabbing version from {toml_file_path}...")
    with open(toml_file_path, "r") as toml_file:
        for line in toml_file.readlines():
            if line.startswith("version = "):
                version = line.split("=")[1].strip().replace('"', "")
                logger.info(f"version found: {version}")
                return version
        raise ValueError(
            "Couldn't find package version within the .toml file.\n"
            "Try giving a value to the --version parameter."
        )


def version_in_file(version: str, file_path: typing.Union[str, Path]) -> bool:
    with open(file_path, "r") as file:
        content = file.read()
    return version in content


def main(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package-name",
        help="name of the package from which the version will be extracted",
    )
    parser.add_argument(
        "--files", nargs="*", help="files in which the version will be checked"
    )
    args = parser.parse_args(argv)

    if args.package_name is None:
        args.version = get_version_from_toml("pyproject.toml")
    else:
        args.version = version(args.package_name)

    if args.files is None:
        raise ValueError(
            "You must provide some files path to check if they contain the "
            "desired version."
        )

    return 0 if check_files(args.files, args.version) else 1
