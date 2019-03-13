from azure.mgmt.keyvault import KeyVaultManagementClient
from ScoutSuite.providers.utils import run_concurrently


class KeyVaultFacade:
    def __init__(self, credentials, subscription_id):
        self._client = KeyVaultManagementClient(credentials, subscription_id)

    async def get_key_vaults(self):
        return await run_concurrently(self._client.vaults.list_by_subscription)
