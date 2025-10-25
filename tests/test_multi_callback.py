"""
Tests for multi_callback functionality.
"""

import click
from click.testing import CliRunner

from click_compose import multi_callback


def test_multi_callback_single_callback() -> None:
    """
    A single callback works correctly.
    """

    def double(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        del ctx, param
        return value * 2

    @click.command()
    @click.option(
        "--num", type=int, callback=multi_callback(callbacks=[double])
    )
    def cmd(num: int) -> None:
        click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=["--num", "5"])
    assert result.exit_code == 0
    assert result.output.strip() == "10"


def test_multi_callback_multiple_callbacks() -> None:
    """
    Multiple callbacks are applied in sequence.
    """

    def double(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        del ctx, param
        return value * 2

    def add_ten(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        del ctx, param
        return value + 10

    @click.command()
    @click.option(
        "--num",
        type=int,
        callback=multi_callback(callbacks=[double, add_ten]),
    )
    def cmd(num: int) -> None:
        click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=["--num", "5"])
    assert result.exit_code == 0
    # (5 * 2) + 10 = 20
    assert result.output.strip() == "20"


def test_multi_callback_with_validation() -> None:
    """
    Validation callbacks can raise exceptions.
    """
    max_value = 100

    def validate_positive(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        del ctx, param
        if value <= 0:
            msg = "Must be positive"
            raise click.BadParameter(message=msg)
        return value

    def validate_max_100(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        del ctx, param
        if value > max_value:
            msg = f"Must be <= {max_value}"
            raise click.BadParameter(message=msg)
        return value

    @click.command()
    @click.option(
        "--num",
        type=int,
        callback=multi_callback(
            callbacks=[validate_positive, validate_max_100]
        ),
    )
    def cmd(num: int) -> None:
        click.echo(message=num)

    runner = CliRunner()

    # Valid value
    result = runner.invoke(cli=cmd, args=["--num", "50"])
    assert result.exit_code == 0
    assert result.output.strip() == "50"

    # Fails first validator
    result = runner.invoke(cli=cmd, args=["--num", "-5"])
    assert result.exit_code != 0
    assert "Must be positive" in result.output

    # Fails second validator
    result = runner.invoke(cli=cmd, args=["--num", "150"])
    assert result.exit_code != 0
    assert "Must be <= 100" in result.output


def test_multi_callback_empty_list() -> None:
    """
    An empty list of callbacks returns the value unchanged.
    """

    @click.command()
    @click.option("--num", type=int, callback=multi_callback(callbacks=[]))
    def cmd(num: int) -> None:
        click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=["--num", "42"])
    assert result.exit_code == 0
    assert result.output.strip() == "42"


def test_multi_callback_with_type_conversion() -> None:
    """
    Callbacks can change the type of the value.
    """

    def to_string(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> str:
        del ctx, param
        return str(object=value)

    def add_suffix(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: str,
    ) -> str:
        del ctx, param
        return f"{value} items"

    @click.command()
    @click.option(
        "--num",
        type=int,
        callback=multi_callback(callbacks=[to_string, add_suffix]),
    )
    def cmd(num: str) -> None:
        click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=["--num", "42"])
    assert result.exit_code == 0
    assert result.output.strip() == "42 items"
