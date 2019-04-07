from msrestazure.azure_exceptions import CloudError

from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerAzureAdAdministrators(AzureResources):
    async def fetch_all(self):
        try:
            await self.facade.sqldatabase.get_server_azure_ad_administrators(
                self.scope['resource_group_name'], self.scope['server_name'])
            self['ad_admin_configured'] = True
        except CloudError:  # no ad admin configured returns a 404 error
            self['ad_admin_configured'] = False
