Contributing
============

Contributions are welcome!
Please open an issue or pull request on GitHub.

Development Setup
-----------------

Clone the repository and install dependencies:

.. code-block:: shell

   $ git clone https://github.com/adamtheturtle/click-compose.git
   $ cd click-compose
   $ uv sync --all-extras

Running Tests
-------------

Run the test suite with pytest:

.. code-block:: shell

   $ uv run pytest

Code Quality
------------

This project uses several tools to maintain code quality:

- ``ruff`` for linting and formatting
- ``mypy`` for type checking
- ``pylint`` for additional linting
- ``pytest`` for testing

Run all checks with pre-commit:

.. code-block:: shell

   $ uv run pre-commit run --all-files
