"""Adds config flow for Blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

import homeassistant.helpers.device_registry as dr
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_DEVICE_ID, Platform
from homeassistant.helpers import selector

from .const import DOMAIN

if TYPE_CHECKING:
    from typing import Any

    from homeassistant.config import ConfigFlowResult


class ReplacedLightsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow."""

    VERSION = 1

    async def async_step_user(
        self, _user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """React to the user setting up the integration manually."""
        return self.async_show_menu(step_id="user", menu_options=["light"])

    async def async_step_light(
        self, user_input: dict | None = None
    ) -> ConfigFlowResult:
        """Let the user choose a light device to add bulb replacement info to."""
        _errors = {}

        if user_input is not None:
            device_registry = dr.async_get(self.hass)
            device_entry = device_registry.async_get(user_input[CONF_DEVICE_ID])
            device_name = device_entry.name
            return self.async_create_entry(title=device_name, data=user_input)

        return self.async_show_form(
            data_schema=vol.Schema(
                {
                    # Offer a selection of all devices which contain a light entity
                    vol.Required(CONF_DEVICE_ID): selector.DeviceSelector(
                        config=selector.DeviceSelectorConfig(
                            entity=[
                                selector.EntityFilterSelectorConfig(
                                    domain=Platform.LIGHT
                                )
                            ]
                        )
                    )
                }
            ),
            errors=_errors,
        )
