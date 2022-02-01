from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from loguru import logger  # type: ignore

from .settings import DEFAULT_FILE_TO_GRAB_VERSION


def version_in_file(version: str, file_path: str | Path) -> bool:
    with open(file_path, "r") as file:
        content = file.read()
    return version in content


def all_files_have_the_version(files_path: Sequence[str | Path], version: str) -> bool:
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


def get_version_from_file(file_path: Path | str) -> str:
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


def version_checker(grab_version_from: Path | str, files: Sequence[str | Path]) -> int:
    version = get_version_from_file(grab_version_from)
    if all_files_have_the_version(files, version):
        return 0
    return 1


def main(argv: Sequence[str] | None = None) -> int:
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

    return version_checker(args.grab_version_from, args.files)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
