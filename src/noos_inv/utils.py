import pathlib
from collections.abc import Mapping
from enum import StrEnum
from typing import NotRequired, TypedDict


class UserType(StrEnum):
    AWS = "AWS"


class PodConfig(TypedDict):
    podNamespace: str
    podPrefix: str
    podPort: int
    localPort: int
    localAddress: NotRequired[str]


type PodsConfig = dict[str, PodConfig]


class PathNotFound(Exception):
    pass


class ValidationError(Exception):
    pass


def check_path(path: str) -> None:
    """Check whether a path exists on a file system."""
    if not pathlib.Path(path).exists():
        raise PathNotFound(f"Incorrect file system path: {path}")


def check_schema(config: object) -> None:
    """Check whether a port-forward configuration is valid."""
    if not isinstance(config, Mapping):
        raise ValidationError("Configuration must be an mapping")
    if len(config) == 0:
        raise ValidationError("Configuration can not be empty")
    for item in config.values():
        if not isinstance(item, Mapping):
            raise ValidationError("Configuration element must be a mapping")
        if not ({"podNamespace", "podPrefix", "podPort", "localPort"} <= set(item.keys())):
            raise ValidationError("Invalid configuration element keys")
