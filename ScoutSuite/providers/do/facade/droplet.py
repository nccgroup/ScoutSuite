from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.do.authentication_strategy import DoCredentials
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.providers.do.facade.utils import DOFacadeUtils


class DropletFacade:
    def __init__(self, credentials: DoCredentials):
        self._credentials = credentials
        self._client = credentials.client
        self.current_page = 1
        self.per_page = 50

    async def get_droplets(self):
        try:
            droplets = await DOFacadeUtils.get_all_from_pagination(
                self._client.droplets.list, self.current_page, self.per_page, "droplets"
            )
            return droplets["droplets"]
        except Exception as e:
            print_exception(f"Failed to get droplets: {e}")
            return []

    async def get_droplet_fwconfig(self, id):
        try:
            filters = {"droplet_id": id}
            droplet_fwconfig = await DOFacadeUtils.get_all_from_pagination(
                self._client.droplets.list_firewalls,
                self.current_page,
                self.per_page,
                "firewalls",
                filters,
            )
            return droplet_fwconfig
        except Exception as e:
            print_exception(f"Failed to get droplet firewall config: {e}")
            return []

    # TODO not required for now
    # async def get_droplet_details(self, id):
    #     try:
    #         droplets = await run_concurrently(lambda: self._client.droplets.list()['droplets'])
    #         return droplets
    #     except Exception as e:
    #         print_exception(f'Failed to get do droplets: {e}')
    #         return []
