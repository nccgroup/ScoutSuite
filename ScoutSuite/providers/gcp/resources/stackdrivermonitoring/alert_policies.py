from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class AlertPolicies(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_alert_policies = await self.facade.stackdrivermonitoring.get_alert_policies(self.project_id)
        for raw_alert_policy in raw_alert_policies:
            alert_policy_name, alert_policy = self._parse_alert_policy(raw_alert_policy)
            self[alert_policy_name] = alert_policy

    def _parse_alert_policy(self, raw_alert_policy):
        alert_policy_dict = {}
        alert_policy_dict['id'] = get_non_provider_id(raw_alert_policy.name)
        alert_policy_dict['name'] = raw_alert_policy.display_name
        alert_policy_dict['combiner'] = raw_alert_policy.combiner
        alert_policy_dict['creation_record'] = raw_alert_policy.creation_record
        alert_policy_dict['mutation_record'] = raw_alert_policy.mutation_record
        alert_policy_dict['conditions'] = raw_alert_policy.conditions
        alert_policy_dict['enabled'] = raw_alert_policy.enabled
        return alert_policy_dict['id'], alert_policy_dict


