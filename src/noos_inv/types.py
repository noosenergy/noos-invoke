from enum import StrEnum
from typing import NotRequired, TypedDict


class PodConfig(TypedDict):
    podNamespace: str
    podPrefix: str
    podPort: int
    localPort: int
    localAddress: NotRequired[str]


type PodsConfig = dict[str, PodConfig]


class UserType(StrEnum):
    AWS = "AWS"
