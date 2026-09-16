Changelog
=========

.. towncrier release notes start

2026.09.16
----------

- Replace ``multi_callback`` with the fully typed binary ``compose_callbacks`` primitive.
  Compose its result again to build pipelines longer than two callbacks.
  The ``deduplicate`` and ``sequence_validator`` helpers now accept the sequence values produced by Click's ``multiple=True`` options rather than optional values.

2026.09.08
----------

- Drop Python 3.10 support (requires Python >=3.11).

2025.10.27.3
------------

2025.10.27.2
------------

2025.10.27.1
------------

2025.10.27
----------

Initial release.

Features:

* ``multi_callback``: Combine multiple Click callbacks into a single callback
* ``sequence_validator``: Apply a validator to each element in a sequence
* Full type hints support
* Full test suite
* Sphinx documentation
