from pathlib import Path

import pytest

from version_checker.main import (
    check_files,
    get_version_from_toml,
    main,
    version_in_file,
)

from .utils import write_something_to_file


def test_version_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version is in the file, 2.0.0")
    assert version_in_file("2.0.0", tmp_file_path)


def test_version_not_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version not in the file")
    assert not version_in_file("2.0.0", tmp_file_path)


def test_cmd_version_not_in_file(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, "version not in the file")
    response = main(["--version", "2.0.0", "--files", str(tmp_file_path)])

    assert response == 1
    assert "❌" in caplog.text


def test_cmd_version_in_file(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, "version is in the file, 2.0.0")
    response = main(["--version", "2.0.0", "--files", str(tmp_file_path)])

    assert response == 0
    assert "✅" in caplog.text


def test_cmd_no_version_provided_as_parameter(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "I don't have any version")
    response = main(["--files", str(tmp_file_path)])
    assert response == 1


def test_cmd_no_files_provided():
    with pytest.raises(ValueError):
        main(["--version", "2.0.0"])


def test_cmd_2_files_provided_one_does_not_contain_the_version(
    tmp_file_path: Path,
):
    write_something_to_file(tmp_file_path, "I have the version: 2.0.0")
    another_file = tmp_file_path.parent / "another_file.txt"
    write_something_to_file(another_file, "I do not have the version")

    response = main(
        [
            "--version",
            "2.0.0",
            "--files",
            str(tmp_file_path),
            str(another_file),
        ]
    )

    assert response == 1


def test_cmd_2_files_provided_both_contain_the_version(tmp_file_path: Path,):
    write_something_to_file(tmp_file_path, "I have the version: 2.0.0")
    another_file = tmp_file_path.parent / "another_file.txt"
    write_something_to_file(another_file, "I have it too: 2.0.0")

    response = main(
        [
            "--version",
            "2.0.0",
            "--files",
            str(tmp_file_path),
            str(another_file),
        ]
    )

    assert response == 0


def test_get_version_from_toml(tmp_file_path: Path, caplog):
    write_something_to_file(
        tmp_file_path, 'name = "version-checker"\nversion = "0.1.0"'
    )

    response = get_version_from_toml(tmp_file_path)

    assert response == "0.1.0"
    assert "version found: 0.1.0" in caplog.text


def test_get_version_from_toml_with_no_version_defined(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, 'name = "version-checker"\n')
    with pytest.raises(ValueError):
        get_version_from_toml(tmp_file_path)


def test_check_files(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, "I have the version 2.0.0")

    result = check_files([tmp_file_path], "2.0.0")

    assert result
    assert f"checking 1/1: {tmp_file_path}" in caplog.text
