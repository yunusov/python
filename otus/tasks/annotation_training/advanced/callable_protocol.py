"""
TODO:

Define a callable type that accepts a string parameter called `name` and returns None.
"""

from typing import Protocol


class SingleStringInput(Protocol):
    def __call__(self, name: str) -> None: ...
