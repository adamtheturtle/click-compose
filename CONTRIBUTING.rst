Contributing
============

Contributions are welcome! This document provides guidelines for contributing to click-compose.

Setting Up Your Development Environment
----------------------------------------

1. Clone the repository:

.. code-block:: shell

   $ git clone https://github.com/adamtheturtle/click-compose.git
   $ cd click-compose

2. Install dependencies with uv:

.. code-block:: shell

   $ uv sync --all-extras

3. Install pre-commit hooks:

.. code-block:: shell

   $ uv run pre-commit install --install-hooks --hook-type pre-commit --hook-type pre-push --hook-type commit-msg

Running Tests
-------------

Run the full test suite:

.. code-block:: shell

   $ make test

Or directly with pytest:

.. code-block:: shell

   $ uv run --extra=dev pytest

Code Quality
------------

This project uses several tools to maintain code quality. Run all checks with:

.. code-block:: shell

   $ make lint

Or run pre-commit hooks manually:

.. code-block:: shell

   $ uv run pre-commit run --all-files

The project uses:

- **ruff** for linting and formatting
- **mypy** and **pyright** for type checking
- **pylint** for additional linting
- **pytest** for testing with 100% coverage requirement

Building Documentation
----------------------

Build the documentation locally:

.. code-block:: shell

   $ make docs

The built documentation will be in ``docs/build/html/``.

Submitting Changes
------------------

1. Fork the repository
2. Create a feature branch (``git checkout -b feature/my-feature``)
3. Make your changes
4. Run tests and linters
5. Commit your changes with a descriptive message
6. Push to your fork
7. Open a pull request

Pull Request Guidelines
-----------------------

- Ensure all tests pass
- Add tests for new functionality
- Update documentation as needed
- Follow the existing code style
- Write clear commit messages

Code of Conduct
---------------

This project follows the Contributor Covenant Code of Conduct. Please read CODE_OF_CONDUCT.rst before contributing.

Questions?
----------

Feel free to open an issue if you have questions or need clarification on anything.
