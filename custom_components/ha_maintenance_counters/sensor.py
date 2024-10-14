"""Sensor platform for maintenance counters."""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_platform

from .const import SERVICE_SET_NUM_REPLACED_LIGHTS
from .entity import ReplacedLightsEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .coordinator import ReplacedLightsCoordinator
    from .data import ReplacedLightsConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ReplacedLightsConfigEntry,
    async_add_entities: entity_platform.AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [ReplacedLightsCounterEntity(hass=hass, coordinator=coordinator)]
    )
    platform = entity_platform.async_get_current_platform()

    # This will call Entity.set_sleep_timer(sleep_time=VALUE)
    platform.async_register_entity_service(
        SERVICE_SET_NUM_REPLACED_LIGHTS,
        {vol.Required("num_replaced_lights"): cv.positive_int},
        "set_num_replaced",
    )
    await entry.runtime_data.coordinator.async_config_entry_first_refresh()


class ReplacedLightsCounterEntity(ReplacedLightsEntity, SensorEntity):
    """Entity counting the number of bulbs replaced for a given light device."""

    _attr_should_poll = False
    _attr_icon = "mdi:lightbulb-multiple-outline"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_state_class = SensorStateClass.TOTAL

    def __init__(
        self, hass: HomeAssistant, coordinator: ReplacedLightsCoordinator
    ) -> None:
        """Create a new ReplacedLightsCounterEntity."""
        entity_type_key = "num_replaced_lights"
        super().__init__(
            hass=hass, coordinator=coordinator, unique_id_fragment=entity_type_key
        )
        self.entity_description = SensorEntityDescription(
            name="replaced light bulbs",
            key=f"{self.coordinator.device_name}_{entity_type_key}",
            translation_key=entity_type_key,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.num_replaced
        self.async_write_ha_state()

    async def set_num_replaced(self, num_replaced_lights: int) -> None:
        """Handle the SERVICE_SET_NUM_REPLACED_LIGHTS action."""
        self.coordinator.num_replaced = num_replaced_lights
        await self.coordinator.async_request_refresh()
