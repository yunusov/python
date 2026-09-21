"""
TODO:

Define a decorator that wraps a function and returns a function with the same signature.
"""

from collections.abc import Callable


def decorator[**P, T](f: Callable[P, T]) -> Callable[P, T]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        return f(*args, **kwargs)

    return inner
