from oci.key_management import KmsManagementClient, KmsVaultClient
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from oci.pagination import list_call_get_all_results

from ScoutSuite.providers.utils import run_concurrently


class KMSFacade:
    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        # FIXME does this require regional support?
        self._vault_client = KmsVaultClient(self._credentials.config)

    async def get_vaults(self):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._vault_client.list_vaults, self._credentials.compartment_id))
        return response.data

    async def get_keys(self, keyvault):
        key_client = KmsManagementClient(self._credentials.config, keyvault['management_endpoint'])
        response = await run_concurrently(
            lambda: list_call_get_all_results(key_client.list_keys, self._credentials.compartment_id))
        return response.data

