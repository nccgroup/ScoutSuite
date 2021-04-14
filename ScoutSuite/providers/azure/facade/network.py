from azure.mgmt.network import NetworkManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class NetworkFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = NetworkManagementClient(self.credentials.get_credentials(),
                                         subscription_id=subscription_id,
                                         user_agent=get_user_agent())
        return client

    async def get_network_watchers(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.network_watchers.list_all())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve network watchers: {e}')
            return []

    async def get_network_security_groups(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.network_security_groups.list_all())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve network security groups: {e}')
            return []

    async def get_application_security_groups(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.application_security_groups.list_all())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve application security groups: {e}')
            return []

    async def get_virtual_networks(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.virtual_networks.list_all())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve virtual networks: {e}')
            return []

    async def get_network_interfaces(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.network_interfaces.list_all())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve network interfaces: {e}')
            return []
