from azure.graphrbac import GraphRbacManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently


class GraphRBACFacade:
    def __init__(self, credentials, tenant_id):
        self._client = GraphRbacManagementClient(credentials, tenant_id=tenant_id)

    async def get_users(self):
        try:
            return await run_concurrently(lambda: list(self._client.users.list()))
        except Exception as e:
            print_exception('Failed to retrieve users: {}'.format(e))
            return []
