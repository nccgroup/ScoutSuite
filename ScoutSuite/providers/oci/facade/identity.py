import asyncio
import functools

from oci.identity import IdentityClient
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from oci.pagination import list_call_get_all_results
# from ScoutSuite.providers.aws.facade.utils import OracleFacadeUtils

from ScoutSuite.providers.utils import run_concurrently


class IdentityFacade:

    def __init__(self, credentials: OracleCredentials):
        self.compartment_id = credentials.compartment_id
        self._client = IdentityClient(credentials.config)

    async def get_users(self):

        response = await run_concurrently(lambda: list_call_get_all_results(self._client.list_users, self.compartment_id))
        return response.data

    async def get_user_api_keys(self, user_id):

        response = await run_concurrently(lambda: list_call_get_all_results(self._client.list_api_keys, user_id))
        return response.data

    async def get_policies(self):

        response = await run_concurrently(lambda: list_call_get_all_results(self._client.list_policies, self.compartment_id))
        return response.data
