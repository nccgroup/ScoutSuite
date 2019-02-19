# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient
from msrestazure.azure_exceptions import CloudError

from ScoutSuite.providers.base.configs.resource_config import ResourceConfig


class ServerAzureAdAdministratorsConfig(ResourceConfig):

    def __init__(self, resource_group_name, server_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name

        self.value = None

    async def fetch_all(self, credentials, regions=None, partition_name='aws', targets=None):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        try:
            self.value = \
                api.server_azure_ad_administrators.get(self.resource_group_name, self.server_name)
                # TODO: await api.server_azure_ad_administrators.get(self.resource_group_name, self.server_name)
        except CloudError:  # no ad admin configured returns a 404 error
            pass
