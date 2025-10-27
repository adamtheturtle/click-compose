"""
Integration tests combining multiple click-compose features.
"""

from pathlib import Path

import click
from click.testing import CliRunner

from click_compose import multi_callback, sequence_validator


def test_multi_callback_with_sequence_validator() -> None:
    """
    multi_callback and sequence_validator can be combined.
    """
    max_value = 100

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

    def validate_max_100(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Validate that value is at most 100."""
        del ctx, param
        if value > max_value:
            msg = f"Must be <= {max_value}"
            raise click.BadParameter(message=msg)
        return value

    combined_validator = multi_callback(
        callbacks=[validate_positive, validate_max_100]
    )

    @click.command()
    @click.option(
        "--nums",
        multiple=True,
        type=int,
        callback=sequence_validator(validator=combined_validator),
    )
    def cmd(nums: tuple[int, ...]) -> None:
        """Test command."""
        click.echo(message=f"Sum: {sum(nums)}")

    runner = CliRunner()

    # Valid values
    result = runner.invoke(
        cli=cmd, args=["--nums", "10", "--nums", "20", "--nums", "30"]
    )
    assert result.exit_code == 0
    assert "Sum: 60" in result.output

    # One value fails first validator
    result = runner.invoke(
        cli=cmd, args=["--nums", "10", "--nums", "-5", "--nums", "30"]
    )
    assert result.exit_code != 0
    assert "Must be positive" in result.output

    # One value fails second validator
    result = runner.invoke(
        cli=cmd, args=["--nums", "10", "--nums", "150", "--nums", "30"]
    )
    assert result.exit_code != 0
    assert "Must be <= 100" in result.output


def test_complex_pipeline() -> None:
    """
    A complex pipeline of transformations and validations.
    """
    min_value = 1
    max_value = 100

    def validate_range(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Validate that value is within the allowed range."""
        del ctx, param
        if not min_value <= value <= max_value:
            msg = f"Must be between {min_value} and {max_value}"
            raise click.BadParameter(message=msg)
        return value

    def double(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> int:
        """Double the value."""
        del ctx, param
        return value * 2

    def to_percentage(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: int,
    ) -> str:
        """Convert value to percentage string."""
        del ctx, param
        return f"{value}%"

    @click.command()
    @click.option(
        "--values",
        multiple=True,
        type=int,
        callback=sequence_validator(
            validator=multi_callback(
                callbacks=[validate_range, double, to_percentage]
            )
        ),
    )
    def cmd(values: tuple[str, ...]) -> None:
        """Test command."""
        for val in values:
            click.echo(message=val)

    runner = CliRunner()

    # Valid values: 50 -> 100%, 25 -> 50%, 10 -> 20%
    result = runner.invoke(
        cli=cmd,
        args=["--values", "50", "--values", "25", "--values", "10"],
    )
    assert result.exit_code == 0
    assert "100%" in result.output
    assert "50%" in result.output
    assert "20%" in result.output

    # Invalid value (out of range)
    result = runner.invoke(cli=cmd, args=["--values", "150"])
    assert result.exit_code != 0
    assert "Must be between 1 and 100" in result.output


def test_real_world_file_validation() -> None:
    """
    A realistic example validating file paths.
    """

    def validate_file_exists(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: str,
    ) -> Path:
        """Validate that file exists."""
        del ctx, param
        path = Path(value)
        if not path.exists():
            msg = f"File not found: {value}"
            raise click.BadParameter(message=msg)
        return path

    def validate_is_file(
        ctx: click.Context | None,
        param: click.Parameter | None,
        value: Path,
    ) -> Path:
        """Validate that path is a file."""
        del ctx, param
        if not value.is_file():
            msg = f"Not a file: {value}"
            raise click.BadParameter(message=msg)
        return value

    @click.command()
    @click.option(
        "--files",
        multiple=True,
        type=str,
        callback=sequence_validator(
            validator=multi_callback(
                callbacks=[validate_file_exists, validate_is_file]
            )
        ),
    )
    def cmd(files: tuple[Path, ...]) -> None:
        """Test command."""
        click.echo(message=f"Processing {len(files)} files")
        for file in files:
            click.echo(message=f"  - {file.name}")

    runner = CliRunner()

    # Test with LICENSE file (should exist)
    result = runner.invoke(cli=cmd, args=["--files", "LICENSE"])
    assert result.exit_code == 0
    assert "Processing 1 files" in result.output
    assert "LICENSE" in result.output

    # Test with non-existent file
    result = runner.invoke(cli=cmd, args=["--files", "nonexistent.txt"])
    assert result.exit_code != 0
    assert "File not found" in result.output

    # Test with directory instead of file
    result = runner.invoke(cli=cmd, args=["--files", "tests"])
    assert result.exit_code != 0
    assert "Not a file" in result.output
