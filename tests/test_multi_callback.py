"""Tests for same-type callback chains."""

from collections.abc import Callable
from typing import assert_type

import click
from click.testing import CliRunner

from click_compose import multi_callback


def test_multi_callback() -> None:
    """All callbacks run in order with the previous result."""

    def double(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Double the value."""
        del ctx, param
        return value * 2

    def add_ten(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Add ten to the value."""
        del ctx, param
        return value + 10

    callback = multi_callback(callbacks=[double, add_ten, double])
    assert_type(
        callback,
        Callable[[click.Context | None, click.Parameter | None, int], int],
    )

    @click.command()
    @click.option("--num", type=int, callback=callback)
    def cmd(num: int) -> None:
        """Test command."""
        click.echo(message=num)

    result = CliRunner().invoke(cli=cmd, args=["--num", "5"])
    assert result.exit_code == 0
    assert result.output.strip() == "40"


def test_multi_callback_empty() -> None:
    """An empty chain returns its input unchanged."""
    callbacks: list[
        Callable[[click.Context | None, click.Parameter | None, str], str]
    ] = []
    callback = multi_callback(callbacks=callbacks)
    assert callback(None, None, "value") == "value"


def test_multi_callback_single() -> None:
    """A single callback is applied once."""

    def upper(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: str,
    ) -> str:
        """Uppercase the value."""
        del ctx, param
        return value.upper()

    callback = multi_callback(callbacks=[upper])
    assert callback(None, None, "value") == "VALUE"
