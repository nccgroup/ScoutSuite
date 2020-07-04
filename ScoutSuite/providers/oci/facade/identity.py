from oci.identity import IdentityClient
from oci.pagination import list_call_get_all_results

from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from ScoutSuite.core.console import print_exception

from ScoutSuite.providers.utils import run_concurrently


class IdentityFacade:
    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._client = IdentityClient(self._credentials.config)

    async def get_users(self):
        try:
            response = await run_concurrently(
                lambda: list_call_get_all_results(self._client.list_users, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            print_exception(f'Failed to retrieve users: {e}')
            return []

    async def get_user_api_keys(self, user_id):
        try:
            response = await run_concurrently(
                lambda: list_call_get_all_results(self._client.list_api_keys, user_id))
            return response.data
        except Exception as e:
            print_exception(f'Failed to retrieve user api keys: {e}')
            return []

    async def get_groups(self):
        try:
            response = await run_concurrently(
                lambda: list_call_get_all_results(self._client.list_groups, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            print_exception(f'Failed to retrieve groups: {e}')
            return []

    async def get_group_users(self, group_id):
        try:
            response = await run_concurrently(
                lambda: list_call_get_all_results(self._client.list_user_group_memberships,
                                                  self._credentials.get_scope(),
                                                  group_id=group_id))
            return response.data
        except Exception as e:
            print_exception(f'Failed to retrieve group users: {e}')
            return []

    async def get_policies(self):
        try:
            response = await run_concurrently(
                lambda: list_call_get_all_results(self._client.list_policies, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            print_exception(f'Failed to retrieve policies: {e}')
            return None

    async def get_authentication_policy(self):
        try:
            response = await run_concurrently(
                lambda: self._client.get_authentication_policy(self._credentials.config['tenancy']))
            return response.data
        except Exception as e:
            print_exception(f'Failed to retrieve authentication policy: {e}')
            return []
