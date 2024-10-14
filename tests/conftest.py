"""common fixtures."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Return the root directory of the ha_maintenance_counters repository."""
    return Path(__file__).parent.parent.resolve()


@pytest.fixture(scope="session")
def integration_root(repo_root: Path) -> Path:
    """Return the directory in which the integration sources live."""
    return repo_root / "custom_components" / "ha_maintenance_counters"
