import argparse
import typing
from pathlib import Path

from loguru import logger  # type: ignore

from .settings import DEFAULT_FILE_TO_GRAB_VERSION


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


def get_version_from_file(file_path: typing.Union[Path, str]) -> str:
    logger.info(f"trying to grab version from {file_path}...")
    with open(file_path, "r") as file:
        for line in file.readlines():
            if line.startswith("version = "):
                version = line.split("=")[1].strip().replace('"', "")
                logger.info(f"version found: {version}")
                return version
        raise ValueError(
            f"Couldn't find package version within the file: {file_path}.\n"
            'Try setting the version in the file like this: version = "0.1.0",'
            " or using another file for --grab-version-from"
        )


def version_in_file(version: str, file_path: typing.Union[str, Path]) -> bool:
    with open(file_path, "r") as file:
        content = file.read()
    return version in content


def main(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grab-version-from",
        help="path to the file from which the version will be extracted",
        default=DEFAULT_FILE_TO_GRAB_VERSION,
    )
    parser.add_argument(
        "--files", nargs="*", help="files in which the version will be checked"
    )
    args = parser.parse_args(argv)

    if not args.files:
        raise ValueError(
            "You must provide some files path to check if they contain the "
            "desired version. E.g.: --files README.md some_package/__init__.py"
        )

    version = get_version_from_file(args.grab_version_from)

    return 0 if check_files(args.files, version) else 1
