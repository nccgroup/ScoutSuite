from oci.key_management import KmsManagementClient
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from oci.pagination import list_call_get_all_results

from ScoutSuite.providers.utils import run_concurrently


class KMSFacade:
    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        # FIXME does this require regional support?
        self._client = KmsManagementClient(self._credentials.config, "https://iaas.uk-london-1.oraclecloud.com")

    async def get_keys(self):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_keys, self._credentials.compartment_id))
        # for some reason it returns a list of chars instead of a string
        return response.data

