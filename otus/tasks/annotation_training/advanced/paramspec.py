"""
TODO:

Add type annotations to the class `Wrap`, so that it can be called with the
same arguments as the function it wraps.
"""

from collections.abc import Callable
from typing import Generic, ParamSpec, TypeVar

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


class Wrap(Generic[F_Spec, F_Return]):
    wrapped_func: Callable[F_Spec, F_Return]

    def __init__(self, func: Callable[F_Spec, F_Return]) -> None:
        if not isinstance(func, Wrap):
            self.wrapped_func = func

    def __call__(
        self,
        *args: F_Spec.args,
        **kwargs: F_Spec.kwargs,
    ) -> F_Return:
        return self.wrapped_func(*args, **kwargs)
