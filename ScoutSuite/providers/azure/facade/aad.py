from azure.graphrbac import GraphRbacManagementClient

from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.utils import get_user_agent


class AADFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self):
        client = GraphRbacManagementClient(self.credentials.get_credentials('aad_graph'),
                                         tenant_id=self.credentials.get_tenant_id())
        client._client.config.add_user_agent(get_user_agent())
        return client

    async def get_users(self):
        try:
            # This filters down the users which are pulled from the directory, otherwise for large tenants this
            # gets out of hands.
            # See https://github.com/nccgroup/ScoutSuite/issues/698
            user_filter = " and ".join([
                'userType eq \'Guest\''
            ])
            return await run_concurrently(lambda: list(self.get_client().users.list(filter=user_filter)))
        except Exception as e:
            print_exception(f'Failed to retrieve users: {e}')
            return []

    async def get_user(self, user_id):
        try:
            return await run_concurrently(lambda: self.get_client().users.get(user_id))
        except Exception as e:
            print_exception(f'Failed to retrieve user {user_id}: {e}')
            return None

    async def get_groups(self):
        try:
            return await run_concurrently(lambda: list(self.get_client().groups.list()))
        except Exception as e:
            print_exception(f'Failed to retrieve groups: {e}')
            return []

    async def get_user_groups(self, user_id):
        try:
            return await run_concurrently(lambda: list(
                self.get_client().users.get_member_groups(object_id=user_id,
                                                          security_enabled_only=False))
                                          )
        except Exception as e:
            print_exception(f'Failed to retrieve user\'s groups: {e}')
            return []

    async def get_service_principals(self):
        try:
            return await run_concurrently(lambda: list(self.get_client().service_principals.list()))
        except Exception as e:
            print_exception(f'Failed to retrieve service principals: {e}')
            return []

    async def get_applications(self):
        try:
            return await run_concurrently(lambda: list(self.get_client().applications.list()))
        except Exception as e:
            print_exception(f'Failed to retrieve applications: {e}')
            return []
