"""Persistent storage."""

import dataclasses
from copy import deepcopy
from typing import Self, TypeVar
from typing import get_args as get_type_args

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import storage

from .const import DOMAIN

DATA_REGISTRY = f"{DOMAIN}_storage"
STORAGE_KEY_PREFIX = f"{DOMAIN}.storage"
SAVE_DELAY_SECONDS = 5


@dataclasses.dataclass
class _DeviceEntry:
    device_id: str


class _DeviceBasedStorage[StoreType: storage.Store, EntryType: _DeviceEntry]:
    def __init__(
        self,
        store_type: type[StoreType],
        entry_type: type[EntryType],
        hass: HomeAssistant,
    ) -> None:
        self.hass = hass
        self.devices: dict[str, EntryType] = {}
        self._store = store_type(
            hass=self.hass,
            version=store_type.VERSION_MAJOR,
            minor_version=store_type.VERSION_MINOR,
            key=f"{STORAGE_KEY_PREFIX}.{store_type.__name__}",
        )
        self._store_type = store_type
        self._entry_type = entry_type

    @callback
    def async_get_device(self, device_id: str) -> EntryType:
        if device_id in self.devices:
            device = self.devices[device_id]
        else:
            # Device does not yet exist -> we need to create it
            device = self._entry_type(device_id=device_id)
            self.devices[device_id] = device
            self._async_schedule_save()
        return deepcopy(device)

    @callback
    def async_store_device(self, device_id: str, device: EntryType) -> None:
        self.devices[device_id] = deepcopy(device)
        self._async_schedule_save()

    async def _async_load(self) -> None:
        """Load the registry of schedule entries."""
        data = await self._store.async_load()

        if data is not None and "devices" in data:
            for device_dict in data["devices"]:
                device = self._entry_type(**device_dict)
                self.devices[device.device_id] = device

    @callback
    def _async_schedule_save(self) -> None:
        self._store.async_delay_save(self._get_data_to_save, SAVE_DELAY_SECONDS)

    def _get_data_to_save(self) -> dict:
        return {
            "devices": [dataclasses.asdict(device) for device in self.devices.values()]
        }


@dataclasses.dataclass
class _LightDeviceEntry(_DeviceEntry):
    num_replaced: int = 0


class _LightDeviceStore(storage.Store):
    """Holds persistent data, may be able to update the schema in the future."""

    VERSION_MAJOR = 1
    VERSION_MINOR = 1


ReplacedLightsStorage = _DeviceBasedStorage[_LightDeviceStore, _LightDeviceEntry]


T = TypeVar("T", bound=_DeviceBasedStorage)


async def async_get_storage(storage_type: type[T], hass: HomeAssistant) -> T:
    """Return storage instance."""
    store_type, entry_type = get_type_args(storage_type)
    store_type_name = type(store_type).__name__

    if DATA_REGISTRY not in hass.data:
        hass.data[DATA_REGISTRY] = {}
    task = hass.data[DATA_REGISTRY].get(store_type_name)

    if task is None:

        async def _load_reg() -> Self:
            storage = storage_type(store_type, entry_type, hass)
            await storage._async_load()  # noqa: SLF001 (this is a member of our own class)
            return storage

        task = hass.data[DATA_REGISTRY][store_type_name] = hass.async_create_task(
            _load_reg()
        )

    return await task
