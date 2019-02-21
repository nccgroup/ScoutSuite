# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resources import Resources


class DatabaseBlobAuditingPolicies(Resources):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

    async def fetch_all(self, credentials):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        policies =\
            api.database_blob_auditing_policies.get(self.resource_group_name, self.server_name, self.database_name)
            # TODO: await api.database_blob_auditing_policies.get(self.resource_group_name, self.server_name, self.database_name)

        self['auditing_enabled'] = self._is_auditing_enabled(policies)

    @staticmethod
    def _is_auditing_enabled(policies):
        return policies.state == "Enabled"
