"""
TODO:

`return_self` should return an instance of the same type as the current enclosed class.
"""

from typing import Self, TypeVar


class Foo:
    def return_self(self) -> Self: ...


class Foo:
    def return_self[T](self: T) -> T: ...


U = TypeVar("U")


class Foo:
    def return_self(self: U) -> U: ...
