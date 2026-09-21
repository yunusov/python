"""
TODO:

Define a decorator that wraps a function and returns a function with the same signature.
The decorator takes an argument `message` of type string
"""

from collections.abc import Callable


def decorator(message: str):
    def dec[**P, T](f: Callable[P, T]) -> Callable[P, T]:
        def inner(*args: P.args, **kwargs: P.kwargs) -> T:
            return f(*args, **kwargs)

        return inner

    return dec
