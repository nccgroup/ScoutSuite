from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class MonitoringAlertPolicies(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_alert_policies = await self.facade.stackdrivermonitoring.get_alert_policies(self.project_id)
        alert_policy = self._parse_alert_policy(raw_alert_policies)
        self[self.project_id] = alert_policy

    def _parse_alert_policy(self, raw_alert_policies):
        alert_policy_dict = {}
        return alert_policy_dict

    def _specific_alert_policy_present(self, alert_policies, alert_policy_value: str):
        for alert_policy in alert_policies:
            for condition in alert_policy.conditions._value:
                if condition.condition_threshold.filter == alert_policy_value and alert_policy.enabled.value:
                    return True
        return False
