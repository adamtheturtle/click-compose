"""
Setup for ``pytest``.
"""

import pytest
from beartype import beartype


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """
    Apply the beartype decorator to all collected test functions.
    """
    for item in items:
        assert isinstance(item, pytest.Function)
        item.obj = beartype(obj=item.obj)
