"""
Composable Click callback utilities for building flexible CLI applications.
"""

from collections.abc import Callable, Sequence
from typing import TypeAlias, TypeVar

import click

__all__ = [
    "multi_callback",
    "sequence_validator",
]

T = TypeVar("T")

# Type alias for Click callbacks
_ClickCallback: TypeAlias = Callable[
    [click.Context | None, click.Parameter | None, T], T
]


def sequence_validator(
    *,
    validator: _ClickCallback[T],
) -> _ClickCallback[Sequence[T]]:
    """Wrap a single-value validator to apply it to a sequence of values.

    This function takes a Click callback that validates a single value and
    returns a new callback that applies the same validation to each element
    in a sequence.

    Args:
        validator: A Click callback that validates a single value of type T.

    Returns:
        A Click callback that validates a sequence of values of type T.
    """

    def callback(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: Sequence[T],
    ) -> Sequence[T]:
        """
        Apply the validator to each element in the sequence.
        """
        return_values: tuple[T, ...] = ()
        for item in value:
            returned_value = validator(ctx, param, item)
            return_values = (*return_values, returned_value)
        return return_values

    return callback


def multi_callback(
    *,
    callbacks: Sequence[_ClickCallback[T]],
) -> _ClickCallback[T]:
    """Create a Click-compatible callback that applies multiple callbacks in
    sequence.

    This function takes a sequence of Click callbacks and returns a new
    callback that applies each callback in order, threading the value through
    each one.

    Args:
        callbacks: A sequence of Click callbacks to apply in order.

    Returns:
        A Click callback that applies all the given callbacks in sequence.
    """

    def callback(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: T,
    ) -> T:
        """
        Apply each callback in sequence to the value.
        """
        for cb in callbacks:
            value = cb(ctx, param, value)
        return value

    return callback
