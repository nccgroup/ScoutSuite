from azure.mgmt.keyvault import KeyVaultManagementClient
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception


class KeyVaultFacade:
    def __init__(self, credentials, subscription_id):
        self._client = KeyVaultManagementClient(credentials, subscription_id)

    async def get_key_vaults(self):
        try:
            return await run_concurrently(
                lambda: list(self._client.vaults.list_by_subscription()))
        except Exception as e:
            print_exception('Failed to retrieve key vaults: {}'.format(e))
            return []
