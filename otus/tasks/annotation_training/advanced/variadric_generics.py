"""
TODO:

Define an `Array` type that supports element-wise addition of arrays with identical dimensions and types.
"""

from typing import Any, Generic, TypeVarTuple, Unpack

Shape = TypeVarTuple("Shape")


class Array(Generic[Unpack[Shape]]):
    def __init__(self, data: Any = None) -> None:
        self.data = [] if data is None else data

    def __add__(self, other: "Array[Unpack[Shape]]") -> "Array[Unpack[Shape]]":
        if not isinstance(other, Array):
            return NotImplemented
        return Array(self._add(self.data, other.data))

    @staticmethod
    def _add(a: Any, b: Any) -> Any:
        if isinstance(a, list) or isinstance(b, list):
            if not (isinstance(a, list) and isinstance(b, list)):
                raise ValueError("Arrays must have identical dimensions")
            if len(a) != len(b):
                raise ValueError("Arrays must have identical dimensions")
            return [Array._add(x, y) for x, y in zip(a, b)]

        if type(a) is not type(b):
            raise TypeError("Arrays must have identical types")
        return a + b

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Array):
            return NotImplemented
        return self.data == other.data

    def __repr__(self) -> str:
        return f"Array({self.data!r})"
