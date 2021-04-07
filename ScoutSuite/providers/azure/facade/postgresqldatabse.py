from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent


class PostgreSQLDatabaseFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = PostgreSQLManagementClient(self.credentials.get_credentials(),
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
            print_exception(f'Failed to retrieve postgresSQL servers: {e}')
            return []

    async def get_config(self, resource_group_name, server_name,
                         subscription_id: str, configuration_name: str):
        try:
            client = self.get_client(subscription_id)
            val = await run_concurrently(
                lambda: client.configurations.get(resource_group_name, server_name, configuration_name)
            )
            return val
        except Exception as e:
            print_exception(f'Failed to retrieve server configuration: {e}')
            return []

    async def get_firewall_rules(self, resource_group_name, server_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.firewall_rules.list_by_server(resource_group_name, server_name))
            )
        except Exception as e:
            print_exception(f'Failed to retrieve firewalls rules: {e}')
            return []
