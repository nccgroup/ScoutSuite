from azure.mgmt.keyvault import KeyVaultManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class KeyVaultFacade:
    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return KeyVaultManagementClient(self.credentials.arm_credentials, subscription_id=subscription_id)

    async def get_key_vaults(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.vaults.list_by_subscription()))
        except Exception as e:
            print_exception('Failed to retrieve key vaults: {}'.format(e))
            return []
