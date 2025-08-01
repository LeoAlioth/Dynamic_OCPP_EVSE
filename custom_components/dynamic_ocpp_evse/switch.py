from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    entity_id = config_entry.data.get("entity_id", "dynamic_ocpp_evse")
    name = config_entry.data["name"]
    async_add_entities([
        AllowGridChargingSwitch(hass, entity_id, name)
    ])

class AllowGridChargingSwitch(SwitchEntity):
    _attr_entity_category = EntityCategory.CONFIG
    def __init__(self, hass, entity_id, name):
        self.hass = hass
        self._attr_name = f"{name} Allow Grid Charging"
        self._attr_unique_id = f"{entity_id}_allow_grid"
        self._state = True  # Default: allow grid charging

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._state = False
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        # Optionally restore previous state
        # last_state = await self.async_get_last_state()
        last_state = self._state
        if last_state is None:
            self._state = True
        self.async_write_ha_state()
