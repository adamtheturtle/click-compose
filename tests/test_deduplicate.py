"""Tests for ``deduplicate`` helper."""

import os

import click
from click.testing import CliRunner
from hypothesis import given, settings
from hypothesis import strategies as st

from click_compose import deduplicate

_HYPOTHESIS_BACKEND = os.environ.get("HYPOTHESIS_BACKEND", "hypothesis")


@settings(backend=_HYPOTHESIS_BACKEND)
@given(values=st.lists(elements=st.text()))
def test_deduplicate_matches_first_occurrences(values: list[str]) -> None:
    """Deduplication preserves the first occurrence of each value."""
    expected: list[str] = []
    for value in values:
        if value not in expected:
            expected.append(value)

    result = deduplicate(ctx=None, param=None, sequence=values)

    assert result == tuple(expected)
    assert deduplicate(ctx=None, param=None, sequence=result) == result


def test_deduplicate_removes_duplicates() -> None:
    """
    Duplicate values are removed while preserving the original
    order.
    """

    @click.command()
    @click.option("--item", multiple=True, callback=deduplicate)
    def cmd(item: tuple[str, ...]) -> None:
        """Echo the unique items."""
        for value in item:
            click.echo(message=value)

    runner = CliRunner()
    args = [
        "--item",
        "alpha",
        "--item",
        "beta",
        "--item",
        "alpha",
        "--item",
        "gamma",
        "--item",
        "beta",
    ]
    result = runner.invoke(cli=cmd, args=args)
    assert result.exit_code == 0
    assert result.output.strip() == "alpha\nbeta\ngamma"


def test_deduplicate_empty_sequence() -> None:
    """An empty sequence is returned unchanged."""

    @click.command()
    @click.option("--item", multiple=True, callback=deduplicate)
    def cmd(item: tuple[str, ...]) -> None:
        """Report the number of values received."""
        click.echo(message=f"Count: {len(item)}")

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=[])
    assert result.exit_code == 0
    assert "Count: 0" in result.output


def test_deduplicate_returns_tuple() -> None:
    """The helper always returns a tuple even when given a list."""
    values = ["alpha", "alpha", "beta"]
    result = deduplicate(ctx=None, param=None, sequence=values)
    assert isinstance(result, tuple)
    assert result == ("alpha", "beta")
