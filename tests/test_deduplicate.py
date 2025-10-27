"""
Tests for ``deduplicate`` helper.
"""

import click
from click.testing import CliRunner

from click_compose import deduplicate


def test_deduplicate_removes_duplicates() -> None:
    """
    Duplicate values are removed while preserving the original order.
    """

    @click.command()
    @click.option("--item", multiple=True, callback=deduplicate)
    def cmd(item: tuple[str, ...]) -> None:
        """
        Echo the unique items.
        """
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
    """
    An empty sequence is returned unchanged.
    """

    @click.command()
    @click.option("--item", multiple=True, callback=deduplicate)
    def cmd(item: tuple[str, ...]) -> None:
        """
        Report the number of values received.
        """
        click.echo(message=f"Count: {len(item)}")

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=[])
    assert result.exit_code == 0
    assert "Count: 0" in result.output


def test_deduplicate_returns_tuple() -> None:
    """
    The helper always returns a tuple even when given a list.
    """
    values = ["alpha", "alpha", "beta"]
    result = deduplicate(ctx=None, param=None, sequence=values)
    assert isinstance(result, tuple)
    assert result == ("alpha", "beta")
