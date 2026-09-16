Usage
=====

|project| provides utilities for composing Click callbacks.

``compose_callbacks``
---------------------

``compose_callbacks`` creates a Click-compatible callback that applies two callbacks in sequence.
Compose its result again to build a longer type-safe pipeline.

.. code-block:: python

   """Example of using compose_callbacks."""

   import click

   from click_compose import compose_callbacks


   def validator1(
       _ctx: click.Context | None,
       _param: click.Parameter | None,
       value: int,
   ) -> int:
       """First validator."""
       return value


   def validator2(
       _ctx: click.Context | None,
       _param: click.Parameter | None,
       value: int,
   ) -> int:
       """Second validator."""
       return value


   def transformer(
       _ctx: click.Context | None,
       _param: click.Parameter | None,
       value: int,
   ) -> int:
       """Transform the value."""
       return value


   @click.command()
   @click.option(
       "--value",
       type=int,
       callback=compose_callbacks(
           first=compose_callbacks(first=validator1, second=validator2),
           second=transformer,
       ),
   )
   def cmd(value: int) -> None:
       """Example command using compose_callbacks."""
       click.echo(message=value)


   if __name__ == "__main__":
       cmd([])

The value is passed through each callback in order, with the output of one callback becoming the input to the next.

``multi_callback``
------------------

``multi_callback`` applies callbacks in order.
Pass a tuple of up to ten callbacks for statically checked type-changing stages.
Each callback must accept the preceding callback's result.
For same-type callbacks, a typed list of any length is supported.
An empty list returns the input unchanged.

.. code-block:: python

   """Example of using multi_callback."""

   import click

   from click_compose import multi_callback


   def double(
       _ctx: click.Context | None, _param: click.Parameter | None, value: int
   ) -> int:
       """Double the value."""
       return value * 2


   def add_ten(
       _ctx: click.Context | None, _param: click.Parameter | None, value: int
   ) -> int:
       """Add ten to the value."""
       return value + 10


   def to_string(
       _ctx: click.Context | None, _param: click.Parameter | None, value: int
   ) -> str:
       """Convert the value to a string."""
       return str(object=value)


   @click.command()
   @click.option(
       "--value",
       type=int,
       callback=multi_callback(callbacks=(double, add_ten, to_string)),
   )
   def cmd(value: str) -> None:
       """Print the transformed value."""
       click.echo(message=value)

``sequence_validator``
----------------------

``sequence_validator`` wraps a single-value validator to apply it to a sequence of values.
This is particularly useful with Click's ``multiple=True`` option parameter.

.. code-block:: python

   """Example of using sequence_validator."""

   import click

   from click_compose import sequence_validator


   def validate_single_value(
       _ctx: click.Context | None, _param: click.Parameter | None, value: int
   ) -> int:
       """Validate a single value."""
       return value


   @click.command()
   @click.option(
       "--values",
       multiple=True,
       type=int,
       callback=sequence_validator(validator=validate_single_value),
   )
   def cmd(values: tuple[int, ...]) -> None:
       """Example command using sequence_validator."""
       click.echo(message=values)

Each element in the sequence is validated individually, and validation errors are raised for the specific element that fails.

``deduplicate``
---------------

``deduplicate`` is a Click callback that removes duplicate values from a sequence while preserving the original order.
This is particularly useful with Click's ``multiple=True`` option parameter when you want to ensure unique values.

.. code-block:: python

   """Example of using ``deduplicate``."""

   import click

   from click_compose import deduplicate


   @click.command()
   @click.option(
       "--tags",
       multiple=True,
       type=str,
       callback=deduplicate,
   )
   def cmd(tags: tuple[str, ...]) -> None:
       """Example command using ``deduplicate``."""
       click.echo(message=f"Unique tags: {', '.join(tags)}")


   if __name__ == "__main__":
       cmd([])

The callback preserves the first occurrence of each value and removes subsequent duplicates.
For example, if a user provides ``--tags foo --tags bar --tags foo``, the result will be ``('foo', 'bar')``.
