from importlib.metadata import version
from pathlib import Path

import pytest

from version_checker.main import (
    check_files,
    get_version_from_file,
    main,
    version_in_file,
)
from version_checker.settings import DEFAULT_FILE_TO_GRAB_VERSION

from .utils import write_something_to_file


def test_version_in_file(tmp_file_path: Path):
    write_something_to_file(
        tmp_file_path, f"version is in the file, {version('version-checker')}"
    )
    assert version_in_file(version("version-checker"), tmp_file_path)


def test_version_not_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version not in the file")
    assert not version_in_file(version("version-checker"), tmp_file_path)


def test_cmd_version_not_in_file(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, "version not in the file")
    response = main(
        [
            "--grab-version-from",
            DEFAULT_FILE_TO_GRAB_VERSION,
            "--files",
            str(tmp_file_path),
        ]
    )

    assert response == 1
    assert "❌" in caplog.text


def test_cmd_version_in_file(tmp_file_path: Path, caplog):
    write_something_to_file(
        tmp_file_path, f"version is in the file, {version('version-checker')}"
    )
    response = main(
        [
            "--grab-version-from",
            DEFAULT_FILE_TO_GRAB_VERSION,
            "--files",
            str(tmp_file_path),
        ]
    )

    assert response == 0
    assert "✅" in caplog.text


def test_cmd_no_version_provided_as_parameter(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "I don't have any version")
    response = main(["--files", str(tmp_file_path)])
    assert response == 1


def test_cmd_no_files_provided(caplog):
    with pytest.raises(ValueError):
        main(["--grab-version-from", DEFAULT_FILE_TO_GRAB_VERSION])


def test_cmd_2_files_provided_one_does_not_contain_the_version(
    tmp_file_path: Path,
):
    write_something_to_file(
        tmp_file_path, f"I have the version: {version('version-checker')}"
    )
    another_file = tmp_file_path.parent / "another_file.txt"
    write_something_to_file(another_file, "I do not have the version")

    response = main(
        [
            "--grab-version-from",
            DEFAULT_FILE_TO_GRAB_VERSION,
            "--files",
            str(tmp_file_path),
            str(another_file),
        ]
    )

    assert response == 1


def test_cmd_2_files_provided_both_contain_the_version(
    tmp_file_path: Path,
):
    write_something_to_file(
        tmp_file_path, f"I have the version: {version('version-checker')}"
    )
    another_file = tmp_file_path.parent / "another_file.txt"
    write_something_to_file(
        another_file, f"I have it too: {version('version-checker')}"
    )

    response = main(
        [
            "--grab-version-from",
            DEFAULT_FILE_TO_GRAB_VERSION,
            "--files",
            str(tmp_file_path),
            str(another_file),
        ]
    )

    assert response == 0


def test_get_version_from_file(tmp_file_path: Path, caplog):
    write_something_to_file(
        tmp_file_path, 'name = "version-checker"\nversion = "0.1.0"'
    )

    response = get_version_from_file(tmp_file_path)

    assert response == "0.1.0"
    assert "version found: 0.1.0" in caplog.text


def test_get_version_from_file_with_no_version_defined(
    tmp_file_path: Path, caplog
):
    write_something_to_file(tmp_file_path, 'name = "version-checker"\n')
    with pytest.raises(ValueError):
        get_version_from_file(tmp_file_path)


def test_check_files(tmp_file_path: Path, caplog):
    write_something_to_file(
        tmp_file_path, f"I have the version {version('version-checker')}"
    )

    result = check_files([tmp_file_path], version("version-checker"))

    assert result
    assert f"checking 1/1: {tmp_file_path}" in caplog.text
