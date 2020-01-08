from azure.mgmt.authorization import AuthorizationManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class ARMFacade:
    def __init__(self, credentials, subscription_id):
        self._subscription_id = subscription_id
        self._client = AuthorizationManagementClient(credentials, subscription_id=subscription_id)

    async def get_roles(self):
        try:
            scope = '/subscriptions/{}'.format(self._subscription_id)
            return await run_concurrently(lambda: list(self._client.role_definitions.list(scope=scope)))
        except Exception as e:
            print_exception('Failed to retrieve roles: {}'.format(e))
            return []

    async def get_role_assignments(self):
        try:
            return await run_concurrently(lambda: list(self._client.role_assignments.list()))
        except Exception as e:
            print_exception('Failed to retrieve role assignments: {}'.format(e))
            return []
