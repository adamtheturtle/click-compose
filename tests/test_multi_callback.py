"""Tests for multi-callback chains."""

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

    callbacks: list[
        Callable[[click.Context | None, click.Parameter | None, int], int]
    ] = [double, add_ten, double]
    callback = multi_callback(callbacks=callbacks)
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

    callback = multi_callback(callbacks=(upper,))
    assert callback(None, None, "value") == "VALUE"


def test_multi_callback_changes_type() -> None:
    """Each tuple element can change the value type."""

    def to_string(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> str:
        """Convert an integer to a string."""
        del ctx, param
        return str(object=value)

    def add_suffix(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: str,
    ) -> str:
        """Add a suffix to a string."""
        del ctx, param
        return f"{value} items"

    callback = multi_callback(callbacks=(to_string, add_suffix))
    assert_type(
        callback,
        Callable[[click.Context | None, click.Parameter | None, int], str],
    )
    assert callback(None, None, 42) == "42 items"


def test_multi_callback_ten_stages() -> None:
    """The longest supported heterogeneous tuple preserves endpoints."""

    def to_string(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> str:
        """Convert an integer to a string."""
        del ctx, param
        return str(object=value)

    def to_integer(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: str,
    ) -> int:
        """Convert a string to an integer."""
        del ctx, param
        return int(value)

    callback = multi_callback(
        callbacks=(
            to_string,
            to_integer,
            to_string,
            to_integer,
            to_string,
            to_integer,
            to_string,
            to_integer,
            to_string,
            to_integer,
        ),
    )
    assert_type(
        callback,
        Callable[[click.Context | None, click.Parameter | None, int], int],
    )
    value = 42
    assert callback(None, None, value) == value


def test_multi_callback_long_same_type_sequence() -> None:
    """Same-type sequences can exceed the heterogeneous overload limit."""

    def increment(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Increment the value."""
        del ctx, param
        return value + 1

    callbacks: list[
        Callable[[click.Context | None, click.Parameter | None, int], int]
    ] = [increment] * 11
    callback = multi_callback(callbacks=callbacks)
    assert_type(
        callback,
        Callable[[click.Context | None, click.Parameter | None, int], int],
    )
    assert callback(None, None, 0) == len(callbacks)
