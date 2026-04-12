from .const import DOMAIN
from .coordinator import NerdaxeCoordinator

async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, entry):
    host = entry.data["host"]

    coordinator = NerdaxeCoordinator(hass, host)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "number", "button"]
    )

    return True