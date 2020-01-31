from azure.mgmt.authorization import AuthorizationManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class ARMFacade:
    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        return AuthorizationManagementClient(self.credentials.arm_credentials, subscription_id=subscription_id)

    async def get_roles(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            scope = '/subscriptions/{}'.format(subscription_id)
            return await run_concurrently(lambda: list(client.role_definitions.list(scope=scope)))
        except Exception as e:
            print_exception('Failed to retrieve roles: {}'.format(e))
            return []

    async def get_role_assignments(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(lambda: list(client.role_assignments.list()))
        except Exception as e:
            print_exception('Failed to retrieve role assignments: {}'.format(e))
            return []
