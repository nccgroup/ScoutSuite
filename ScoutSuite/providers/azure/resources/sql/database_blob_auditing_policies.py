# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ..resources import AzureSimpleResources


class DatabaseBlobAuditingPolicies(AzureSimpleResources):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

    # TODO: make it really async.
    async def get_resources_from_api(self, credentials):
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)
        return api.database_blob_auditing_policies.get(
            self.resource_group_name, self.server_name, self.database_name)

    def parse_resource(self, policies):
        return 'auditing_enabled', policies.state == "Enabled"
