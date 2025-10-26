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

   import click
   from click_compose import multi_callback

   def validate_positive(ctx, param, value):
       if value <= 0:
           raise click.BadParameter("Must be positive")
       return value

   def validate_max_100(ctx, param, value):
       if value > 100:
           raise click.BadParameter("Must be <= 100")
       return value

   @click.command()
   @click.option(
       "--count",
       type=int,
       callback=multi_callback([validate_positive, validate_max_100]),
   )
   def cmd(count):
       click.echo(f"Count: {count}")

sequence_validator
~~~~~~~~~~~~~~~~~~

Apply a validator to each element in a sequence (useful with ``multiple=True``):

.. code-block:: python

   import click
   from click_compose import sequence_validator

   def validate_positive(ctx, param, value):
       if value <= 0:
           raise click.BadParameter("Must be positive")
       return value

   @click.command()
   @click.option(
       "--numbers",
       multiple=True,
       type=int,
       callback=sequence_validator(validate_positive),
   )
   def cmd(numbers):
       click.echo(f"Sum: {sum(numbers)}")

Documentation
-------------

See the `full documentation <https://adamtheturtle.github.io/click-compose/>`__.
