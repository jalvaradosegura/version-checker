from pathlib import Path

from version_checker.main import main, version_in_file
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
