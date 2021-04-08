from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class Alerts(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_alert in await self.facade.securitycenter.get_alerts(self.subscription_id):
            id, alert = self._parse_alert(raw_alert)
            self[id] = alert

    def _parse_alert(self, alert):
        alert_dict = {}
        alert_dict['id'] = get_non_provider_id(alert.id)
        alert_dict['name'] = alert.name
        return alert_dict['id'], alert_dict
