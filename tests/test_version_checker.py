from pathlib import Path

import pytest

from version_checker.main import main, version_in_file, get_version_from_toml
from .utils import write_something_to_file


def test_version_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version is in the file, 2.0.0")
    assert version_in_file("2.0.0", tmp_file_path)


def test_version_not_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version not in the file")
    assert not version_in_file("2.0.0", tmp_file_path)


def test_cmd_version_not_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version not in the file")
    response = main(["--version", "2.0.0", "--files", str(tmp_file_path)])
    assert response == 1


def test_cmd_version_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "version is in the file, 2.0.0")
    response = main(["--version", "2.0.0", "--files", str(tmp_file_path)])
    assert response == 0


def test_cmd_no_version_provided_as_parameter(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "I don't have any version")
    response = main(["--files", str(tmp_file_path)])
    assert response == 1


def test_get_version_from_toml(tmp_file_path: Path):
    write_something_to_file(
        tmp_file_path, 'name = "version-checker"\nversion = "0.1.0"'
    )
    response = get_version_from_toml(tmp_file_path)
    assert response == "0.1.0"


def test_get_version_from_toml_with_no_version_defined(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, 'name = "version-checker"\n')
    with pytest.raises(ValueError):
        get_version_from_toml(tmp_file_path)
