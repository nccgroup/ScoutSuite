from azure.mgmt.network import NetworkManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class NetworkFacade:
    def __init__(self, credentials, subscription_id):
        self._client = NetworkManagementClient(credentials, subscription_id)

    async def get_network_watchers(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.network_watchers.list_all())
            )
        except Exception as e:
            print_exception('Failed to retrieve network watchers: {}'.format(e))
            return []

    async def get_network_security_groups(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.network_security_groups.list_all())
            )
        except Exception as e:
            print_exception('Failed to retrieve network security groups: {}'.format(e))
            return []

    async def get_virtual_networks(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.virtual_networks.list_all())
            )
        except Exception as e:
            print_exception('Failed to retrieve virtual networks: {}'.format(e))
            return []

    async def get_network_interfaces(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.network_interfaces.list_all())
            )
        except Exception as e:
            print_exception('Failed to retrieve network interfaces: {}'.format(e))
            return []