"""
TODO:

Annotate class `MyContainer`, which should support item access, i.e.
using `[x]` to get, set, and delete an item.

HINT: Use https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
"""

from _typeshed import SupportsItemAccess


class MyContainer(SupportsItemAccess[str | int, int]):
    def __contains__(self, x: object, /) -> bool: ...

    def __getitem__(self, key: str | int, /) -> int: ...

    def __setitem__(self, key: str | int, value: int, /) -> None: ...

    def __delitem__(self, key: str | int, /) -> None: ...
