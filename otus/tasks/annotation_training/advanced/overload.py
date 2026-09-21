"""
TODO:

`process` is a function that takes one argument `response`
- When `response` is bytes, `process` returns a string
- When `response` is an integer, `process` returns tuple[int, str]
- When `response` is None, `process` returns None
"""

from typing import overload


@overload
def process(response: int) -> tuple[int, str]: ...


@overload
def process(response: bytes) -> str: ...


@overload
def process(response: None) -> None: ...


def process(response: int | bytes | None) -> str | None | tuple[int, str]: ...
