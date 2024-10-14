"""
Custom Home Assistant integration for tracking maintenance work.

For more details about this integration, please refer to
https://github.com/sleiner/ha_maintenance_counters
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import CONF_DEVICE_ID, Platform
from homeassistant.helpers import config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .const import DATA_STORE_REPLACED_LIGHTS, DOMAIN
from .coordinator import ReplacedLightsCoordinator
from .data import ReplacedLightsRuntimeData
from .store import ReplacedLightsStorage, async_get_storage

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.typing import ConfigType

    from .data import ReplacedLightsConfigEntry

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.SENSOR,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # noqa: ARG001
    """Set up this integration."""
    hass.data[DOMAIN] = {
        DATA_STORE_REPLACED_LIGHTS: await async_get_storage(ReplacedLightsStorage, hass)
    }

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ReplacedLightsConfigEntry,
) -> bool:
    """Set up a configuration entry for this integration using the UI."""
    entry.runtime_data = ReplacedLightsRuntimeData(
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=ReplacedLightsCoordinator(
            hass,
            config_entry=entry,
            device_id=entry.data[CONF_DEVICE_ID],
            store=hass.data[DOMAIN][DATA_STORE_REPLACED_LIGHTS],
        ),
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ReplacedLightsConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ReplacedLightsConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
