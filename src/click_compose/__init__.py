"""
Composable Click callback utilities for building flexible CLI applications.
"""

from collections.abc import Callable, Sequence
from typing import TypeVar

import click
from beartype import beartype

T = TypeVar("T")
U = TypeVar("U")


@beartype
def sequence_validator(
    *,
    validator: Callable[[click.Context | None, click.Parameter | None, T], U],
) -> Callable[
    [click.Context | None, click.Parameter | None, Sequence[T]], Sequence[U]
]:
    """Wrap a single-value validator to apply it to a sequence of values.

    This function takes a Click callback that validates a single value and
    returns a new callback that applies the same validation to each element
    in a sequence. The validator can transform the type of each element.

    Args:
        validator: A Click callback that validates a single value.

    Returns:
        A Click callback that validates a sequence of values.
    """

    def callback(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: Sequence[T],
    ) -> Sequence[U]:
        """
        Apply the validator to each element in the sequence.
        """
        return_values: tuple[U, ...] = ()
        for item in value:
            returned_value = validator(ctx, param, item)
            return_values = (*return_values, returned_value)
        return return_values

    return callback


@beartype
def deduplicate(
    ctx: click.Context | None,
    param: click.Parameter | None,
    sequence: Sequence[T],
) -> Sequence[T]:
    """
    Return the sequence with duplicates removed while preserving order.
    """
    # We "use" the parameters to silence unused-argument tooling.
    del ctx
    del param

    return tuple(dict.fromkeys(sequence).keys())


@beartype
def multi_callback(
    *,
    callbacks: Sequence[Callable[..., T]],
) -> Callable[[click.Context | None, click.Parameter | None, T], T]:
    """Create a Click-compatible callback that applies multiple callbacks in
    sequence.

    This function takes a sequence of Click callbacks and returns a new
    callback that applies each callback in order, threading the value through
    each one. Each callback can transform the type, allowing for flexible
    pipelines of transformations and validations.

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
        result = value
        for cb in callbacks:
            result = cb(ctx, param, result)
        return result

    return callback
