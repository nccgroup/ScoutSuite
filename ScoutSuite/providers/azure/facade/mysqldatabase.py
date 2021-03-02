from azure.mgmt.rdbms.mysql import MySQLManagementClient
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent


class MySQLDatabaseFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = MySQLManagementClient(self.credentials.get_credentials(),
                                       subscription_id=subscription_id,
                                       user_agent=get_user_agent())
        return client

    async def get_servers(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.servers.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve mySQL servers: {e}')
            return []
