"""Tests for sequence_validator functionality."""

import click
from click.testing import CliRunner
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

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=_identity),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        """Test command."""
        for num in nums:
            click.echo(message=num)

    args: list[str] = []
    for item in items:
        args.extend(["--nums", str(object=item)])

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=args)
    assert result.exit_code == 0
    expected = "\n".join(str(object=x) for x in items)
    assert result.output.strip() == expected


@given(items=st.lists(elements=st.integers()))
def test_maps_function_over_elements(items: list[int]) -> None:
    """Sequence_validator(f)(items) == [f(item) for item in items]."""

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=_double),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        """Test command."""
        for num in nums:
            click.echo(message=num)

    args: list[str] = []
    for item in items:
        args.extend(["--nums", str(object=item)])

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=args)
    assert result.exit_code == 0
    expected = "\n".join(str(object=x * 2) for x in items)
    assert result.output.strip() == expected


@given(items=st.lists(elements=st.integers()))
def test_preserves_length(items: list[int]) -> None:
    """Output length matches input length."""

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=_identity),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        """Test command."""
        click.echo(message=len(nums))

    args: list[str] = []
    for item in items:
        args.extend(["--nums", str(object=item)])

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=args)
    assert result.exit_code == 0
    assert result.output.strip() == str(object=len(items))


@given(items=st.lists(elements=st.integers()))
def test_preserves_order(items: list[int]) -> None:
    """Element order is preserved."""

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=_identity),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        """Test command."""
        click.echo(message=",".join(str(object=n) for n in nums))

    args: list[str] = []
    for item in items:
        args.extend(["--nums", str(object=item)])

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=args)
    assert result.exit_code == 0
    expected = ",".join(str(object=x) for x in items)
    assert result.output.strip() == expected


def test_empty_sequence() -> None:
    """Empty sequence returns empty sequence."""

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=_identity),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        """Test command."""
        click.echo(message=f"Count: {len(nums)}")

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=[])
    assert result.exit_code == 0
    assert "Count: 0" in result.output


def test_none_returns_none() -> None:
    """None input returns None."""

    @click.command()
    @click.option(
        "--num",
        type=int,
        default=None,
        callback=sequence_validator(
            validator=lambda _c, _p, v: v,
        ),
    )
    def cmd(num: int | None) -> None:
        """Test command."""
        click.echo(message=f"Value: {num}")

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=[])
    assert result.exit_code == 0
    assert "Value: None" in result.output


def test_sequence_validator_with_validation() -> None:
    """Validation errors are raised for individual elements."""

    def validate_positive(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Validate that value is positive."""
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
        """Test command."""
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


def test_sequence_validator_with_type_conversion() -> None:
    """Validators can convert types for each element."""

    def to_string(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> str:
        """Convert value to string."""
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
        """Test command."""
        for num in nums:
            click.echo(message=num)

    runner = CliRunner()
    result = runner.invoke(cli=cmd, args=["--nums", "1", "--nums", "2"])
    assert result.exit_code == 0
    assert result.output.strip() == "Number: 1\nNumber: 2"
