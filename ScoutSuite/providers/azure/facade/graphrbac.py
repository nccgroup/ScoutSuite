from azure.graphrbac import GraphRbacManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class GraphRBACFacade:
    def __init__(self, graphrbac_credentials, credentials, tenant_id, subscription_id):
        self._subscription_id = subscription_id
        self._client = GraphRbacManagementClient(graphrbac_credentials, tenant_id=tenant_id, base_url=graphrbac_credentials.cloud_environment.endpoints.resource_manager)
        self._authorization_client = AuthorizationManagementClient(credentials, subscription_id=subscription_id, base_url=credentials.cloud_environment.endpoints.resource_manager)

    async def get_users(self):
        try:
            return await run_concurrently(lambda: list(self._client.users.list()))
        except Exception as e:
            print_exception('Failed to retrieve users: {}'.format(e))
            return []

    async def get_groups(self):
        try:
            return await run_concurrently(lambda: list(self._client.groups.list()))
        except Exception as e:
            print_exception('Failed to retrieve groups: {}'.format(e))
            return []

    async def get_user_groups(self, user_id):
        try:
            return await run_concurrently(lambda: list(
                self._client.users.get_member_groups(object_id=user_id,
                                                     security_enabled_only=False))
                                          )
        except Exception as e:
            print_exception('Failed to retrieve user\'s groups: {}'.format(e))
            return []

    async def get_service_principals(self):
        try:
            return await run_concurrently(lambda: list(self._client.service_principals.list()))
        except Exception as e:
            print_exception('Failed to retrieve service principals: {}'.format(e))
            return []

    async def get_applications(self):
        try:
            return await run_concurrently(lambda: list(self._client.applications.list()))
        except Exception as e:
            print_exception('Failed to retrieve applications: {}'.format(e))
            return []

    async def get_roles(self):
        try:
            scope = '/subscriptions/{}'.format(self._subscription_id)
            return await run_concurrently(lambda: list(self._authorization_client.role_definitions.list(scope=scope)))
        except Exception as e:
            print_exception('Failed to retrieve roles: {}'.format(e))
            return []

    async def get_role_assignments(self):
        try:
            return await run_concurrently(lambda: list(self._authorization_client.role_assignments.list()))
        except Exception as e:
            print_exception('Failed to retrieve role assignments: {}'.format(e))
            return []
