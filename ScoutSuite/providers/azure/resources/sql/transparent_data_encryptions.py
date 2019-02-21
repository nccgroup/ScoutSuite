# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient

from ScoutSuite.providers.base.configs.resources import Resources


class TransparentDataEncryptions(Resources):

    def __init__(self, resource_group_name, server_name, database_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.database_name = database_name

        self.value = None

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        encryptions =\
            api.transparent_data_encryptions.get(self.resource_group_name, self.server_name, self.database_name)
            # TODO: await api.transparent_data_encryptions.get(self.resource_group_name, self.server_name, self.database_name)

        self['transparent_data_encryption_enabled'] = self._is_transparent_data_encryption_enabled(encryptions)

    @staticmethod
    def _is_transparent_data_encryption_enabled(encryptions):
        return encryptions.status == "Enabled"
