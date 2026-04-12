from homeassistant.components.number import NumberEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        NerdaxeNumber(hass, entry, "Fan Speed", "manualFanSpeed", 0, 100, 1),
        NerdaxeNumber(hass, entry, "Frequency", "frequency", 100, 800, 5),
        NerdaxeNumber(hass, entry, "Core Voltage", "coreVoltage", 800, 1500, 10),
    ])


class NerdaxeNumber(NumberEntity):
    def __init__(self, hass, entry, name, key, min_v, max_v, step):
        self.hass = hass
        self.entry = entry
        self._name = f"NerdAxe {name}"
        self._key = key
        self._min = min_v
        self._max = max_v
        self._step = step

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        coordinator = self.hass.data[DOMAIN][self.entry.entry_id]
        return coordinator.data.get(self._key)

    @property
    def min_value(self):
        return self._min

    @property
    def max_value(self):
        return self._max

    @property
    def step(self):
        return self._step

    @property
    def mode(self):
        return "slider"

    async def async_set_value(self, value):
        host = self.entry.data["host"]
        session = async_get_clientsession(self.hass)

        payload = {self._key: int(value)}

        # special case: fan control (disable auto)
        if self._key == "manualFanSpeed":
            payload["autofanspeed"] = 0

        await session.patch(
            f"http://{host}/api/system",
            json=payload
        )

        # refresh data after change
        coordinator = self.hass.data[DOMAIN][self.entry.entry_id]
        await coordinator.async_request_refresh()