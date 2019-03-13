from azure.mgmt.network import NetworkManagementClient
from ScoutSuite.providers.utils import run_concurrently


class NetworkFacade:
    def __init__(self, credentials, subscription_id):
        self._client = NetworkManagementClient(credentials, subscription_id)

    async def get_network_watchers(self):
        return await run_concurrently(self._client.network_watchers.list_all)

    async def get_network_security_groups(self):
        return await run_concurrently(self._client.network_security_groups.list_all)
