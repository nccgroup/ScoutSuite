# -*- coding: utf-8 -*-

from msrestazure.azure_exceptions import CloudError

from ScoutSuite.providers.base.configs.resources import Resources


class ServerAzureAdAdministrators(Resources):

    def __init__(self, resource_group_name, server_name, facade):
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.facade = facade

    # TODO: make it really async.
    async def fetch_all(self):
        try:
            self.facade.server_azure_ad_administrators.get(self.resource_group_name, self.server_name)
            self['ad_admin_configured'] = True
        except CloudError:  # no ad admin configured returns a 404 error
            self['ad_admin_configured'] = False
