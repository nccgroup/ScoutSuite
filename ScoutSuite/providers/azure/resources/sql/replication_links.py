# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ..resources import AzureSimpleResources


class ReplicationLinks(AzureSimpleResources):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

    # TODO: make it really async.
    async def get_resources_from_api(self, credentials):
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)
        return list(api.replication_links.list_by_database(
            self.resource_group_name, self.server_name, self.database_name))

    def parse_resource(self, links):
        return 'replication_configured', len(links) > 0
