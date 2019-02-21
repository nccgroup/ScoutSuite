# -*- coding: utf-8 -*-

from azure.mgmt.sql import SqlManagementClient
from msrestazure.azure_exceptions import CloudError

from ScoutSuite.providers.base.configs.resources import Resources


class ServerAzureAdAdministrators(Resources):

    def __init__(self, resource_group_name, server_name):
        self.resource_group_name = resource_group_name
        self.server_name = server_name

    async def fetch_all(self, credentials):
        # sdk container:
        api = SqlManagementClient(credentials.credentials, credentials.subscription_id)

        try:
            admins = \
                api.server_azure_ad_administrators.get(self.resource_group_name, self.server_name)
                # TODO: await api.server_azure_ad_administrators.get(self.resource_group_name, self.server_name)
            self['ad_admin_configured'] = True
        except CloudError:  # no ad admin configured returns a 404 error
            self['ad_admin_configured'] = False
