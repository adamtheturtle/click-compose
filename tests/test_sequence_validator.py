"""
Tests for sequence_validator functionality.
"""

import click
from click.testing import CliRunner

from click_compose import sequence_validator


def test_sequence_validator_basic() -> None:
    """
    A validator is applied to each element in a sequence.
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
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=double),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        for num in nums:
            click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(
        cli=cmd, args=["--nums", "1", "--nums", "2", "--nums", "3"]
    )
    assert result.exit_code == 0
    assert result.output.strip() == "2\n4\n6"


def test_sequence_validator_with_validation() -> None:
    """
    Validation errors are raised for individual elements.
    """

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

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=validate_positive),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        for num in nums:
            click.echo(message=num)

    runner = CliRunner()

    # Valid values
    result = runner.invoke(
        cli=cmd, args=["--nums", "1", "--nums", "2", "--nums", "3"]
    )
    assert result.exit_code == 0
    assert result.output.strip() == "1\n2\n3"

    # Invalid value
    result = runner.invoke(
        cli=cmd, args=["--nums", "1", "--nums", "-5", "--nums", "3"]
    )
    assert result.exit_code != 0
    assert "Must be positive" in result.output


def test_sequence_validator_empty_sequence() -> None:
    """
    An empty sequence is handled correctly.
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
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=double),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        click.echo(message=f"Count: {len(nums)}")

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=[])
    assert result.exit_code == 0
    assert "Count: 0" in result.output

    # Also test with non-empty sequence to cover the double function
    result = runner.invoke(cli=cmd, args=["--nums", "5"])
    assert result.exit_code == 0
    assert "Count: 1" in result.output


def test_sequence_validator_with_type_conversion() -> None:
    """
    Validators can convert types for each element.
    """

    def to_string(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> str:
        del ctx, param
        return f"Number: {value}"

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=to_string),
    )
    def cmd(nums: tuple[str, ...]) -> None:
        for num in nums:
            click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=["--nums", "1", "--nums", "2"])
    assert result.exit_code == 0
    assert result.output.strip() == "Number: 1\nNumber: 2"


def test_sequence_validator_preserves_order() -> None:
    """
    The order of elements is preserved.
    """

    def identity(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        del ctx, param
        return value

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=identity),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        click.echo(message=",".join(str(object=n) for n in nums))

    runner = CliRunner()
    result = runner.invoke(
        cli=cmd,
        args=["--nums", "5", "--nums", "2", "--nums", "8", "--nums", "1"],
    )
    assert result.exit_code == 0
    assert result.output.strip() == "5,2,8,1"
