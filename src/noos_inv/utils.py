import pathlib
from enum import StrEnum


class UserType(StrEnum):
    AWS = "AWS"


class PathNotFound(Exception):
    pass


def check_path(path: str) -> None:
    """Check whether a path exists on a file system."""
    if not pathlib.Path(path).exists():
        raise PathNotFound(f"Incorrect file system path: {path}")
