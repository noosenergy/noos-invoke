import pathlib
from collections.abc import Mapping
from enum import StrEnum
from typing import TypedDict


class UserType(StrEnum):
    AWS = "AWS"


class PodConfig(TypedDict):
    pod_namespace: str
    pod_prefix: str
    pod_port: int
    local_port: int


type ServicesConfig = dict[str, PodConfig]


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
        if set(item.keys()) != {"pod_namespace", "pod_prefix", "pod_port", "local_port"}:
            raise ValidationError("Invalid configuration element keys")
