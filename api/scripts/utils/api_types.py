""" Represents the return type / result of the API call. """
from dataclasses import dataclass
from collections.abc import Mapping


@dataclass
class Result:
    pretty: Mapping[str, str | list[str]]
    image: str
    answer: str | list[str] | None = None


@dataclass
class Error:
    name: str
    message: str


Response = Result | Error
