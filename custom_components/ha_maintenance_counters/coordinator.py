"""Data update coordinator."""

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

from .const import DOMAIN, LOGGER
from .data import ReplacedLightsConfigEntry
from .store import ReplacedLightsStorage


class ReplacedLightsCoordinator(DataUpdateCoordinator):
    """Coordinates the data exchange between platforms and persistent storage."""

    def __init__(
        self,
        hass: HomeAssistant,
        device_id: str,
        store: ReplacedLightsStorage,
        config_entry: ReplacedLightsConfigEntry,
    ) -> None:
        """Initialize."""
        super().__init__(hass=hass, logger=LOGGER, name=DOMAIN)
        self.config_entry = config_entry
        self.device_id = device_id
        self._store = store

    async def _async_update_data(self) -> None:
        return

    @property
    def num_replaced(self) -> int:
        """Return the number of replaced bulbs for a given device."""
        return self._store.async_get_device(self.device_id).num_replaced

    @num_replaced.setter
    def num_replaced(self, value: int) -> None:
        device = self._store.async_get_device(self.device_id)
        device.num_replaced = value
        self._store.async_store_device(device_id=self.device_id, device=device)

    @property
    def device_name(self) -> str:
        """Return the name corresponding to this coordinator object."""
        device_entry = self.async_get_device_entry()
        return device_entry.name_by_user or device_entry.name

    @callback
    def async_get_device_entry(self) -> dr.DeviceEntry:
        """Return the device entry corresponding to this coordinator object."""
        device_registry = dr.async_get(self.hass)
        return device_registry.async_get(self.device_id)
