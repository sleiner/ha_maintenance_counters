"""Button platform for maintenance counters."""

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ReplacedLightsCoordinator
from .data import ReplacedLightsConfigEntry
from .entity import ReplacedLightsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ReplacedLightsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [LightbulbReplacedButton(hass=hass, coordinator=coordinator)],
    )
    await coordinator.async_config_entry_first_refresh()


class LightbulbReplacedButton(ReplacedLightsEntity, ButtonEntity):
    """A button whose press means that a light bulb was replaced."""

    _attr_should_poll = False
    _attr_icon = "mdi:autorenew"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self, hass: HomeAssistant, coordinator: ReplacedLightsCoordinator
    ) -> None:
        """Create a new LightbulbReplacedButton object."""
        entity_type_key = "bulb_replaced"
        super().__init__(
            hass=hass, coordinator=coordinator, unique_id_fragment=entity_type_key
        )
        self.entity_description = ButtonEntityDescription(
            name="bulb replaced",
            key=f"{self.coordinator.device_name}_{entity_type_key}",
            translation_key=entity_type_key,
        )

    async def async_press(self) -> None:
        """Press the button."""
        self.coordinator.num_replaced += 1
        await self.coordinator.async_request_refresh()
