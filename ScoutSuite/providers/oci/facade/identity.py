from oci.identity import IdentityClient
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from oci.pagination import list_call_get_all_results

from ScoutSuite.providers.utils import run_concurrently


class IdentityFacade:
    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._client = IdentityClient(self._credentials.config)

    async def get_users(self):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_users, self._credentials.compartment_id))
        return response.data

    async def get_user_api_keys(self, user_id):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_api_keys, user_id))
        return response.data

    async def get_groups(self):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_groups, self._credentials.compartment_id))
        return response.data

    async def get_group_users(self, group_id):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_user_group_memberships,
                                              self._credentials.compartment_id,
                                              group_id=group_id))
        return response.data

    async def get_policies(self):
        response = await run_concurrently(
            lambda: list_call_get_all_results(self._client.list_policies, self._credentials.compartment_id))
        return response.data

    async def get_authentication_policy(self):
        response = await run_concurrently(
            lambda: self._client.get_authentication_policy(self._credentials.compartment_id))
        return response.data
