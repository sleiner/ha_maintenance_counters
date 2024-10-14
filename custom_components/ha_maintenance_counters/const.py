"""Constants for ha_maintenance_counters."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

DOMAIN: Final = "ha_maintenance_counters"

DATA_STORE_REPLACED_LIGHTS = "store_replaced_lights"
CONF_SOURCE_ENTITY_ID: Final = "source_entity_id"

SERVICE_SET_NUM_REPLACED_LIGHTS = "set_num_replaced_lights"
