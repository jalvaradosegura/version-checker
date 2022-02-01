import sys

if sys.version_info < (3, 8):  # pragma: no cover
    from typing_extensions import Final
else:
    from typing import Final

DEFAULT_FILE_TO_GRAB_VERSION: Final = "pyproject.toml"
