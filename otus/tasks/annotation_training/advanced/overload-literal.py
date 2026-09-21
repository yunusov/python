"""
TODO:

foo is a function that returns an integer when second argument is 1, returns a string when second argument is 2, returns a list when second argument is 3, otherwise it returns the first argument.
"""

from typing import Any, Literal, overload


@overload
def foo(value, flag: Literal[1]) -> int: ...


@overload
def foo(value, flag: Literal[2]) -> str: ...


@overload
def foo(value, flag: Literal[3]) -> list: ...


@overload
def foo[T](value: T, flag: Any) -> T:
    return value


def foo(value, flag: Literal[1, 2, 3] | Any) -> int | str | list | Any: ...
