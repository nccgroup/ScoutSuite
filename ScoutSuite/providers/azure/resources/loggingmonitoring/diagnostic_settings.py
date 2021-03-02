from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class DiagnosticSettings(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for diagnostic_setting in await self.facade.loggingmonitoring.get_diagnostic_settings(self.subscription_id):
            id, diagnostic_settings = self._parse_diagnostic_settings(diagnostic_setting)
            self[id] = diagnostic_settings

    def _parse_diagnostic_settings(self, diagnostic_setting):
        diagnostic_setting_dict = {}

        diagnostic_setting_dict['id'] = diagnostic_setting.id
        diagnostic_setting_dict['name'] = diagnostic_setting.name
        diagnostic_setting_dict['storage_account_id'] = diagnostic_setting.storage_account_id

        return diagnostic_setting_dict['id'], diagnostic_setting_dict


