"""
TODO:

Modify `foo` so it takes an argument of arbitrary type.
"""

from typing import Any


def foo(v: Any[int | str]):
    """⬆️ Change b me. No need to implement the function."""


l = [2, 3, 4]
foo(1)
foo("10")
foo(l)
foo(1, 2)
