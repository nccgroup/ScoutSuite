# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resources import Resources


class DatabaseThreatDetectionPolicies(Resources):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

    async def fetch_all(self, credentials):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        policies =\
            api.database_threat_detection_policies.get(self.resource_group_name, self.server_name, self.database_name)
            # TODO: await api.transparent_data_encryptions.get(self.resource_group_name, self.server_name, self.database_name)

        self['threat_detection_enabled'] = self._is_threat_detection_enabled(policies)

    @staticmethod
    def _is_threat_detection_enabled(policies):
        return policies.state == "Enabled"
