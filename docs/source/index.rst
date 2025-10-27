|project|
=========

Composable Click callback utilities for building flexible CLI applications.

.. include:: install.rst

.. include:: usage.rst

API Reference
-------------

.. automodule:: click_compose
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

Combining Multiple Validators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``multi_callback`` to apply multiple validation functions in sequence:

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

Validating Sequences
~~~~~~~~~~~~~~~~~~~~

Use ``sequence_validator`` to apply a validator to each element in a sequence:

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

Combining Both
~~~~~~~~~~~~~~

Combine both utilities for powerful validation pipelines:

.. code-block:: python

   import click
   from click_compose import multi_callback, sequence_validator

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
       "--numbers",
       multiple=True,
       type=int,
       callback=sequence_validator(
           multi_callback([validate_positive, validate_max_100])
       ),
   )
   def cmd(numbers):
       click.echo(f"Valid numbers: {numbers}")

Reference
---------

.. toctree::
   :maxdepth: 3

   install
   usage
   changelog
