from azure.mgmt.sql import SqlManagementClient
from ScoutSuite.providers.utils import run_concurrently


class SQLDatabaseFacade:
    def __init__(self, credentials, subscription_id):
        self._client = SqlManagementClient(credentials, subscription_id)

    async def get_database_blob_auditing_policies(self, resource_group_name, server_name, database_name):
        return await run_concurrently(
            lambda: self._client.database_blob_auditing_policies.get(
                resource_group_name, server_name, database_name)
        )

    async def get_database_threat_detection_policies(self, resource_group_name, server_name, database_name):
        return await run_concurrently(
            lambda: self._client.database_threat_detection_policies.get(
                resource_group_name, server_name, database_name)
        )

    async def get_databases(self, resource_group_name, server_name):
        return await run_concurrently(
            lambda: self._client.databases.list_by_server(resource_group_name, server_name)
        )

    async def get_database_replication_links(self, resource_group_name, server_name, database_name):
        return await run_concurrently(
            lambda: list(self._client.replication_links.list_by_database(
                resource_group_name, server_name, database_name))
        )

    async def get_server_azure_ad_administrators(self, resource_group_name, server_name):
        return await run_concurrently(
            lambda: self._client.server_azure_ad_administrators.get(resource_group_name, server_name)
        )

    async def get_servers(self):
        return await run_concurrently(self._client.servers.list)

    async def get_database_transparent_data_encryptions(self, resource_group_name, server_name, database_name):
        return await run_concurrently(
            lambda: self._client.transparent_data_encryptions.get(
                resource_group_name, server_name, database_name)
        )
