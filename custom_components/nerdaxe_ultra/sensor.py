from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        NerdaxeSensor(coordinator, "Temperature", "temp", "°C"),
        NerdaxeSensor(coordinator, "Power", "power", "W"),
        NerdaxeSensor(coordinator, "Current", "currentA", "A"),
        NerdaxeSensor(coordinator, "Hashrate", "hashRate", "GH/s"),
        NerdaxeSensor(coordinator, "Hashrate 1m", "hashRate_1m", "GH/s"),
        NerdaxeSensor(coordinator, "Hashrate 10m", "hashRate_10m", "GH/s"),
        NerdaxeSensor(coordinator, "Shares Accepted", "sharesAccepted", ""),
        NerdaxeSensor(coordinator, "Shares Rejected", "sharesRejected", ""),
        NerdaxeEfficiencySensor(coordinator),
    ]

    async_add_entities(sensors)


class NerdaxeSensor(SensorEntity):
    def __init__(self, coordinator, name, key, unit):
        self.coordinator = coordinator
        self._name = f"NerdAxe {name}"
        self._key = key
        self._unit = unit

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.coordinator.data.get(self._key)

    @property
    def unit_of_measurement(self):
        return self._unit

    async def async_update(self):
        await self.coordinator.async_request_refresh()


class NerdaxeEfficiencySensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator

    @property
    def name(self):
        return "NerdAxe Efficiency"

    @property
    def state(self):
        power = self.coordinator.data.get("power", 0)
        hashrate = self.coordinator.data.get("hashRate", 0)

        if power > 0:
            return round(hashrate / power, 2)
        return 0

    @property
    def unit_of_measurement(self):
        return "GH/W"

    async def async_update(self):
        await self.coordinator.async_request_refresh()