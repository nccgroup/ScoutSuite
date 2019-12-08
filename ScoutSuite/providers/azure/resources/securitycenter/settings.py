from ScoutSuite.providers.azure.resources.base import AzureResources


class Settings(AzureResources):
    async def fetch_all(self):
        for raw_settings in await self.facade.securitycenter.get_settings():
            id, settings = self._parse_settings(
                raw_settings)
            self[id] = settings

    def _parse_settings(self, settings):
        settings_dict = {}
        return settings_dict['id'], settings_dict
