Usage
=====

|project| provides utilities for composing Click callbacks.

``multi_callback``
------------------

``multi_callback`` creates a Click-compatible callback that applies multiple callbacks in sequence.
This is useful when you want to apply multiple transformations or validators to a single value.

.. code-block:: python

   from click_compose import multi_callback

   @click.command()
   @click.option(
       "--value",
       type=int,
       callback=multi_callback([validator1, validator2, transformer]),
   )
   def cmd(value):
       click.echo(value)

The value is passed through each callback in order, with the output of one callback becoming the input to the next.

``sequence_validator``
----------------------

``sequence_validator`` wraps a single-value validator to apply it to a sequence of values.
This is particularly useful with Click's ``multiple=True`` option parameter.

.. code-block:: python

   from click_compose import sequence_validator

   @click.command()
   @click.option(
       "--values",
       multiple=True,
       type=int,
       callback=sequence_validator(validate_single_value),
   )
   def cmd(values):
       click.echo(values)

Each element in the sequence is validated individually, and validation errors are raised for the specific element that fails.
