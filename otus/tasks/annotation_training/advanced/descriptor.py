"""
TODO:

Create a descriptor and annotate the __get__ method.
"""

from typing import Any, Generic, TypeVar, overload

T = TypeVar("T")


class Descriptor(Generic[T]):
    @overload
    def __get__(self, instance: None, owner: Any) -> Descriptor:
        """you don't need to implement this"""

    @overload
    def __get__(self, instance: object, owner: Any | None = None) -> str:
        """you don't need to implement this"""

    def __get__(
        self, instance: object | None, owner: Any | None = None
    ) -> str | Descriptor:
        """you don't need to implement this"""
