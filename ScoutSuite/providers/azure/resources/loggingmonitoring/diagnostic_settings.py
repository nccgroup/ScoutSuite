from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class DiagnosticSettings(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        diagnostic_dict = {}
        diagnostic_dict['diagnostic_exist'] = await self.facade.loggingmonitoring.get_subscription_diagnostic_settings(
            self.subscription_id) != []
        self[self.subscription_id] = diagnostic_dict
