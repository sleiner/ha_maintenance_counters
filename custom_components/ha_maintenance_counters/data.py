"""Custom types for maintenance counters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .coordinator import ReplacedLightsCoordinator


type ReplacedLightsConfigEntry = ConfigEntry[ReplacedLightsRuntimeData]


@dataclass
class ReplacedLightsRuntimeData:
    """Data for the maintenance counters integration."""

    integration: Integration
    coordinator: ReplacedLightsCoordinator
