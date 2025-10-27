click-compose
=============

Composable Click callback utilities for building flexible CLI applications.

.. contents::
   :local:

Installation
------------

.. code-block:: shell

   $ pip install click-compose

Or with ``uv``:

.. code-block:: shell

   $ uv add click-compose

Quick Start
-----------

``click-compose`` provides two main utilities for composing Click callbacks:

multi_callback
~~~~~~~~~~~~~~

Combine multiple callbacks into a single callback that applies them in sequence:

.. code-block:: python

   """Example of using multi_callback to combine validators."""

   import click

   from click_compose import multi_callback


   def validate_positive(
       _ctx: click.Context,
       _param: click.Parameter,
       value: int,
   ) -> int:
       """Validate that value is positive."""
       if value <= 0:
           msg = "Must be positive"
           raise click.BadParameter(msg)
       return value


   MAX_VALUE = 100


   def validate_max_100(
       _ctx: click.Context,
       _param: click.Parameter,
       value: int,
   ) -> int:
       """Validate that value is at most 100."""
       if value > MAX_VALUE:
           msg = "Must be <= 100"
           raise click.BadParameter(msg)
       return value


   @click.command()
   @click.option(
       "--count",
       type=int,
       callback=multi_callback([validate_positive, validate_max_100]),
   )
   def cmd(count: int) -> None:
       """Example command with multiple validators."""
       click.echo(f"Count: {count}")


   if __name__ == "__main__":
       cmd()

sequence_validator
~~~~~~~~~~~~~~~~~~

Apply a validator to each element in a sequence (useful with ``multiple=True``):

.. code-block:: python

   """Example of using sequence_validator with multiple values."""

   import click

   from click_compose import sequence_validator


   def validate_positive(
       _ctx: click.Context,
       _param: click.Parameter,
       value: int,
   ) -> int:
       """Validate that value is positive."""
       if value <= 0:
           msg = "Must be positive"
           raise click.BadParameter(msg)
       return value


   @click.command()
   @click.option(
       "--numbers",
       multiple=True,
       type=int,
       callback=sequence_validator(validate_positive),
   )
   def cmd(numbers: tuple[int, ...]) -> None:
       """Example command with sequence validation."""
       click.echo(f"Sum: {sum(numbers)}")


   if __name__ == "__main__":
       cmd()

Documentation
-------------

See the `full documentation <https://adamtheturtle.github.io/click-compose/>`__.
