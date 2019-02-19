# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resource_config import ResourceConfig


class ReplicationLinksConfig(ResourceConfig):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

        self.value = None

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        self.value =\
            list(api.replication_links.list_by_database(self.resource_group_name, self.server_name, self.database_name))
            # TODO: await api.replication_links.list_by_databases(self.resource_group_name, self.server_name, self.database_name)
