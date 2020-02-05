from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class Settings(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Settings, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_settings in await self.facade.securitycenter.get_settings(self.subscription_id):
            id, settings = self._parse_settings(
                raw_settings)
            self[id] = settings

    def _parse_settings(self, settings):
        settings_dict = {}
        return settings_dict['id'], settings_dict
