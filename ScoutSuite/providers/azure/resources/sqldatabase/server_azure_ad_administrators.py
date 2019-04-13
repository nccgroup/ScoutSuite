from msrestazure.azure_exceptions import CloudError

from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerAzureAdAdministrators(AzureResources):
    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str):
        self.facade = facade
        self.resource_group_name = resource_group_name
        self.server_name = server_name

    async def fetch_all(self):
        try:
            await self.facade.sqldatabase.get_server_azure_ad_administrators(
                self.resource_group_name, self.server_name)
            self['ad_admin_configured'] = True
        except CloudError:  # no ad admin configured returns a 404 error
            self['ad_admin_configured'] = False
