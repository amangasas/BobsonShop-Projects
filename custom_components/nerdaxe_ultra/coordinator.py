from datetime import timedelta
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

class NerdaxeCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host):
        self.host = host
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            logger=None,
            name="nerdaxe_ultra",
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self):
        url = f"http://{self.host}/api/system/info"
        with async_timeout.timeout(5):
            resp = await self.session.get(url)
            return await resp.json()