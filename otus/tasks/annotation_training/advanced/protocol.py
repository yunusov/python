"""
TODO:
    Define a protocol for class `SupportsQuack` that supports a "quack" method.
"""

from typing import Protocol


class SupportsQuack(Protocol):
    def quack(self) -> None: ...
