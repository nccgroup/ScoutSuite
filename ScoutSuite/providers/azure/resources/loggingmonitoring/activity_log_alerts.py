from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class ActivityLogAlerts(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for log_alert in await self.facade.loggingmonitoring.get_activity_log_alerts(self.subscription_id):
            id, log_alerts = self._parse_log_alerts(log_alert)
            self[id] = log_alerts

    def _parse_log_alerts(self, log_alert):
        log_alert_dict = {}

        log_alert_dict['id'] = log_alert.id
        log_alert_dict['name'] = log_alert.name

        return log_alert_dict['id'], log_alert_dict


