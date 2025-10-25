"""
Pytest configuration and fixtures for click-compose tests.
"""

import pytest


@pytest.fixture
def sample_value() -> int:
    """
    Provide a sample integer value for testing.
    """
    return 42
