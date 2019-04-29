from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerAzureAdAdministrators(AzureResources):
    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str):
        super(ServerAzureAdAdministrators, self).__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name

    async def fetch_all(self):
        raw_ad_admins = await self.facade.sqldatabase.get_server_azure_ad_administrators(
            self.resource_group_name, self.server_name)
        if len(raw_ad_admins) > 0:
            self['ad_admin_configured'] = True
        else:
            self['ad_admin_configured'] = False
