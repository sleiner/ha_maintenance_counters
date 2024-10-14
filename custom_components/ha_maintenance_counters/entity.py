"""BlueprintEntity class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers import entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .coordinator import ReplacedLightsCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


class ReplacedLightsEntity(CoordinatorEntity[ReplacedLightsCoordinator]):
    """Base class for all entities created by the maintenance counters integration."""

    _attr_has_entity_name = True
    _attr_entity_category = entity.EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: ReplacedLightsCoordinator,
        unique_id_fragment: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id + unique_id_fragment
        self.hass = hass

        device_entry = self.coordinator.async_get_device_entry()
        self._attr_device_info = entity.DeviceInfo(
            connections=device_entry.connections,
            identifiers=device_entry.identifiers,
        )
