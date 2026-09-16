"""
Composable Click callback utilities for building flexible CLI
applications.
"""

from collections.abc import Callable, Sequence
from typing import TypeAlias, TypeVar, overload

import click
from beartype import beartype

T = TypeVar("T")
U = TypeVar("U")
_T0 = TypeVar("_T0")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_T6 = TypeVar("_T6")
_T7 = TypeVar("_T7")
_T8 = TypeVar("_T8")
_T9 = TypeVar("_T9")
_T10 = TypeVar("_T10")

_ClickCallback: TypeAlias = Callable[
    [click.Context | None, click.Parameter | None, T], U
]


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


# Finite overloads check each type transition in a callback chain.
# https://github.com/python/mypy/issues/8449
# https://discuss.python.org/t/proposal-feedback-wanted-typing-relatedtypes-typing-relation-enables-type-hinting-variadic-compose-etc/56698
@overload
def multi_callback(
    *,
    callbacks: tuple[_ClickCallback[_T0, _T1],],
) -> _ClickCallback[_T0, _T1]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
    ],
) -> _ClickCallback[_T0, _T2]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
    ],
) -> _ClickCallback[_T0, _T3]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
    ],
) -> _ClickCallback[_T0, _T4]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
        _ClickCallback[_T4, _T5],
    ],
) -> _ClickCallback[_T0, _T5]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
        _ClickCallback[_T4, _T5],
        _ClickCallback[_T5, _T6],
    ],
) -> _ClickCallback[_T0, _T6]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
        _ClickCallback[_T4, _T5],
        _ClickCallback[_T5, _T6],
        _ClickCallback[_T6, _T7],
    ],
) -> _ClickCallback[_T0, _T7]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
        _ClickCallback[_T4, _T5],
        _ClickCallback[_T5, _T6],
        _ClickCallback[_T6, _T7],
        _ClickCallback[_T7, _T8],
    ],
) -> _ClickCallback[_T0, _T8]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
        _ClickCallback[_T4, _T5],
        _ClickCallback[_T5, _T6],
        _ClickCallback[_T6, _T7],
        _ClickCallback[_T7, _T8],
        _ClickCallback[_T8, _T9],
    ],
) -> _ClickCallback[_T0, _T9]: ...


@overload
def multi_callback(
    *,
    callbacks: tuple[
        _ClickCallback[_T0, _T1],
        _ClickCallback[_T1, _T2],
        _ClickCallback[_T2, _T3],
        _ClickCallback[_T3, _T4],
        _ClickCallback[_T4, _T5],
        _ClickCallback[_T5, _T6],
        _ClickCallback[_T6, _T7],
        _ClickCallback[_T7, _T8],
        _ClickCallback[_T8, _T9],
        _ClickCallback[_T9, _T10],
    ],
) -> _ClickCallback[_T0, _T10]: ...


@overload
def multi_callback(
    *,
    callbacks: list[_ClickCallback[T, T]],
) -> _ClickCallback[T, T]: ...


@beartype
def multi_callback(
    *,
    callbacks: Sequence[Callable[..., object]],
) -> Callable[..., object]:
    """Apply Click callbacks in order.

    Tuple literals of up to ten callbacks preserve intermediate types
    under static type checking. A typed list of callbacks with a shared
    input and output type may have any length. An empty list produces an
    identity callback.

    Args:
        callbacks: The callbacks to apply, in order.

    Returns:
        A Click callback that applies every callback in sequence.
    """

    def callback(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: object,
    ) -> object:
        """Apply each callback to the preceding result."""
        for item in callbacks:
            value = item(ctx, param, value)
        return value

    return callback
