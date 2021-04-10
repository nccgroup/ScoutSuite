from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class FirewallRules(AzureResources):

    def __init__(self, facade: AzureFacade, resource_group_name: str, server_name: str, subscription_id: str):
        super().__init__(facade)
        self.resource_group_name = resource_group_name
        self.server_name = server_name
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for firewall_rule in await self.facade.sqldatabase.get_firewall_rules(self.resource_group_name, self.server_name,
                                                                         self.subscription_id):
            id, firewall_rules = self._parse_firewall_rules(firewall_rule)
            self[id] = firewall_rules

    def _parse_firewall_rules(self, firewall_rule):
        firewall_rules_dict ={}
        firewall_rules_dict['id'] = get_non_provider_id(firewall_rule.id.lower())
        firewall_rules_dict['name'] = firewall_rule.name
        firewall_rules_dict['start_ip'] = firewall_rule.start_ip_address
        firewall_rules_dict['end_ip'] = firewall_rule.end_ip_address

        return firewall_rules_dict['id'], firewall_rules_dict
