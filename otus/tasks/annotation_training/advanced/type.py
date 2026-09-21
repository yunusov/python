"""
TODO:

`make_object` takes a class returns an instance of it.
"""


def make_object[T](cls: type[T]) -> T:
    return cls()
