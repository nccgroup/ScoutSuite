from azure.mgmt.keyvault import KeyVaultManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class KeyVaultFacade:

    def __init__(self, credentials, resource_group=None):
        self.credentials = credentials
        self.resource_group = resource_group

    def get_client(self, subscription_id: str):
        client = KeyVaultManagementClient(self.credentials.get_credentials(),
                                          subscription_id=subscription_id, user_agent=get_user_agent())
        return client

    async def get_key_vaults(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            
            if self.resource_group:
                return await run_concurrently(
                    lambda: list(client.vaults.list_by_resource_group(self.resource_group)))
            else:
                return await run_concurrently(
                    lambda: list(client.vaults.list_by_subscription()))
        except Exception as e:
            print_exception(f'Failed to retrieve key vaults: {e}')
            return []
