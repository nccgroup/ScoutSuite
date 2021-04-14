
from azure.mgmt.sql import SqlManagementClient
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception
from ScoutSuite.utils import get_user_agent


class SQLDatabaseFacade:

    def __init__(self, credentials):
        self.credentials = credentials

    def get_client(self, subscription_id: str):
        client = SqlManagementClient(self.credentials.get_credentials(),
                                     subscription_id=subscription_id,
                                     user_agent=get_user_agent())

        return client

    async def get_database_blob_auditing_policies(self, resource_group_name, server_name, database_name,
                                                  subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.database_blob_auditing_policies.get(
                    resource_group_name, server_name, database_name)
            )
        except Exception as e:
            print_exception(f'Failed to retrieve database blob auditing policies: {e}')
            return []

    async def get_database_threat_detection_policies(self, resource_group_name, server_name, database_name,
                                                     subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.database_threat_detection_policies.get(resource_group_name, server_name, database_name,
                                                                      'default')
            )
        except Exception as e:
            print_exception(f'Failed to retrieve database threat detection policies: {e}')
            return []

    async def get_databases(self, resource_group_name, server_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.databases.list_by_server(resource_group_name, server_name))
            )
        except Exception as e:
            print_exception(f'Failed to retrieve databases: {e}')
            return []

    async def get_database_replication_links(self, resource_group_name, server_name, database_name,
                                             subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.replication_links.list_by_database(
                    resource_group_name, server_name, database_name)
            )
        except Exception as e:
            print_exception(f'Failed to retrieve database replication links: {e}')
            return []

    async def get_server_azure_ad_administrators(self, resource_group_name, server_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.server_azure_ad_administrators.list_by_server(resource_group_name, server_name)
            )
        except Exception as e:
            print_exception(f'Failed to retrieve server azure ad administrators: {e}')
            return None

    async def get_server_blob_auditing_policies(self, resource_group_name, server_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.server_blob_auditing_policies.get(resource_group_name, server_name)
            )
        except Exception as e:
            print_exception(f'Failed to retrieve server blob auditing policies: {e}')
            return []

    async def get_server_security_alert_policies(self, resource_group_name, server_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.server_security_alert_policies.get(resource_group_name, server_name, 'default')
            )
        except Exception as e:
            print_exception(f'Failed to retrieve server security alert policies: {e}')
            return []

    async def get_servers(self, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: list(client.servers.list())
            )
        except Exception as e:
            print_exception(f'Failed to retrieve servers: {e}')
            return []

    async def get_database_transparent_data_encryptions(self, resource_group_name, server_name, database_name,
                                                        subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.transparent_data_encryptions.get(
                    resource_group_name, server_name, database_name, 'current')
            )
        except Exception as e:
            print_exception(f'Failed to retrieve database transparent data encryptions: {e}')
            return []

    async def get_server_vulnerability_assessments(self, resource_group_name, server_name,
                                                   subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.server_vulnerability_assessments.get(resource_group_name, server_name, 'default')
            )
        except Exception as e:
            print_exception(f'Failed to retrieve server vulnerability assessments: {e}')

    async def get_server_encryption_protectors(self, resource_group_name, server_name, subscription_id: str):
        try:
            client = self.get_client(subscription_id)
            return await run_concurrently(
                lambda: client.encryption_protectors.get(resource_group_name, server_name, 'current')
            )
        except Exception as e:
            print_exception(f'Failed to retrieve database transparent data encryptions: {e}')
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
