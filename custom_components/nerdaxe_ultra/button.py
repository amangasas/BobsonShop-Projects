import aiohttp
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([NerdaxeRestartButton(entry)])


class NerdaxeRestartButton(ButtonEntity):
    def __init__(self, entry):
        self.entry = entry

    @property
    def name(self):
        return "NerdAxe Restart"

    async def async_press(self):
        host = self.entry.data["host"]

        async with aiohttp.ClientSession() as session:
            await session.post(f"http://{host}/api/system/restart")