"""Property-based tests for sequence_validator using Hypothesis."""

import click
from hypothesis import given
from hypothesis import strategies as st

from click_compose import sequence_validator


def _identity(
    ctx: click.Context | None,
    param: click.Parameter | None,
    value: int,
) -> int:
    """Return value unchanged."""
    del ctx, param
    return value


def _double(
    ctx: click.Context | None,
    param: click.Parameter | None,
    value: int,
) -> int:
    """Double the value."""
    del ctx, param
    return value * 2


@given(items=st.lists(elements=st.integers()))
def test_identity_preserves_values(items: list[int]) -> None:
    """Sequence_validator with identity returns the same values."""
    result = sequence_validator(validator=_identity)(None, None, items)
    assert result is not None
    assert list(result) == items


@given(items=st.lists(elements=st.integers()))
def test_maps_function_over_elements(items: list[int]) -> None:
    """Sequence_validator(f)(items) == [f(item) for item in items]."""
    result = sequence_validator(validator=_double)(None, None, items)
    assert result is not None
    assert list(result) == [x * 2 for x in items]


@given(items=st.lists(elements=st.integers()))
def test_preserves_length(items: list[int]) -> None:
    """Output length matches input length."""
    result = sequence_validator(validator=_identity)(None, None, items)
    assert result is not None
    assert len(list(result)) == len(items)


@given(items=st.lists(elements=st.integers()))
def test_preserves_order(items: list[int]) -> None:
    """Element order is preserved."""
    result = sequence_validator(validator=_identity)(None, None, items)
    assert result is not None
    assert list(result) == items


def test_empty_sequence() -> None:
    """Empty sequence returns empty sequence."""
    result = sequence_validator(validator=_identity)(None, None, [])
    assert result is not None
    assert not list(result)


def test_none_returns_none() -> None:
    """None input returns None."""
    result = sequence_validator(validator=_identity)(None, None, None)
    assert result is None
