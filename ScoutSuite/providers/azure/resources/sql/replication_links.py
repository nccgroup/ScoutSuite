# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resources import Resources


class ReplicationLinks(Resources):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        links =\
            list(api.replication_links.list_by_database(self.resource_group_name, self.server_name, self.database_name))
            # TODO: await api.replication_links.list_by_databases(self.resource_group_name, self.server_name, self.database_name)

        self['replication_configured'] = self._is_replication_configured(links)

    @staticmethod
    def _is_replication_configured(links):
        return len(links) > 0
