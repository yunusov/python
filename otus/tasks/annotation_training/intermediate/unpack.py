"""
TODO:

`foo` expects two keyword arguments - `name` of type `str`, and `age` of type `int`.
"""

from typing import TypedDict


class Person(TypedDict):
    name: str
    age: int


def foo(name: str, age: int): ...
