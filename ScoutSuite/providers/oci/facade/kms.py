from oci.key_management import KmsManagementClient, KmsVaultClient
from oci.pagination import list_call_get_all_results

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.providers.utils import run_concurrently


class KMSFacade:
    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._vault_client = KmsVaultClient(self._credentials.config)

    async def get_vaults(self):
        try:
            response = await run_concurrently(
                lambda: list_call_get_all_results(self._vault_client.list_vaults, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            print_exception(f'Failed to get KMS vaults: {e}')
            return []

    async def get_keys(self, keyvault):
        try:
            key_client = KmsManagementClient(self._credentials.config, keyvault['management_endpoint'])
            response = await run_concurrently(
                lambda: list_call_get_all_results(key_client.list_keys, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            print_exception(f'Failed to get KMS vaults: {e}')
            return []
