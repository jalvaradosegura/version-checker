from pathlib import Path

import pytest


@pytest.fixture
def tmp_file_path(tmp_path: Path) -> Path:
    file_path = tmp_path / "file.txt"
    return file_path
