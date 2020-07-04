from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ServerAzureAdAdministrators(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        self['ad_admin'] = await self.facade.sqldatabase.get_server_azure_ad_administrators(
            self.resource_group_name, self.server_name, self.subscription_id)
