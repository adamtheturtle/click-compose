"""
Composable Click callback utilities for building flexible CLI
applications.
"""

from collections.abc import Callable, Sequence
from typing import TypeVar

import click
from beartype import beartype

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


@beartype
def sequence_validator(
    *,
    validator: Callable[[click.Context | None, click.Parameter | None, T], U],
) -> Callable[
    [click.Context | None, click.Parameter | None, Sequence[T]],
    Sequence[U],
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
        """Apply the validator to each element in the sequence."""
        return_values: list[U] = []
        for item in value:
            returned_value = validator(ctx, param, item)
            return_values.append(returned_value)
        return return_values

    return callback


@beartype
def deduplicate(
    ctx: click.Context | None,
    param: click.Parameter | None,
    sequence: Sequence[T],
) -> Sequence[T]:
    """
    Return the sequence with duplicates removed while preserving
    order.
    """
    # We "use" the parameters to silence unused-argument tooling.
    del ctx
    del param

    return tuple(dict.fromkeys(sequence).keys())


@beartype
def compose_callbacks(
    *,
    first: Callable[[click.Context | None, click.Parameter | None, T], U],
    second: Callable[[click.Context | None, click.Parameter | None, U], V],
) -> Callable[[click.Context | None, click.Parameter | None, T], V]:
    """Compose two Click callbacks into one callback.

    The first callback's output is passed to the second callback. Compose the
    result again to build a longer pipeline while preserving every
    intermediate type.

    Args:
        first: The callback to apply first.
        second: The callback to apply to the first callback's result.

    Returns:
        A Click callback that applies both callbacks in sequence.
    """

    def callback(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: T,
    ) -> V:
        """Apply both callbacks in sequence to the value."""
        intermediate = first(ctx, param, value)
        return second(ctx, param, intermediate)

    return callback
