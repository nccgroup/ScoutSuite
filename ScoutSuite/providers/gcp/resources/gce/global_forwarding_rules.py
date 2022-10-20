from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class GlobalForwardingRules(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_rules = await self.facade.gce.get_global_forwarding_rules(self.project_id)
        for raw_rule in raw_rules:
            try:
                rule_id, rule = self._parse_forwarding_rule(raw_rule)
            except Exception as e:
                print(e)
            self[rule_id] = rule

    def _parse_forwarding_rule(self, raw_global_forwarding_rule):
        global_forwarding_rule_dict = {}
        global_forwarding_rule_dict['id'] = raw_global_forwarding_rule.get("id")
        global_forwarding_rule_dict['name'] = raw_global_forwarding_rule.get("name")
        global_forwarding_rule_dict['creation_timestamp'] = raw_global_forwarding_rule.get("creationTimestamp")
        global_forwarding_rule_dict['description'] = raw_global_forwarding_rule.get("description")
        global_forwarding_rule_dict['ip_address'] = raw_global_forwarding_rule.get("IPAddress")
        global_forwarding_rule_dict['ip_protocol'] = raw_global_forwarding_rule.get("IPProtocol")
        global_forwarding_rule_dict['port_range'] = raw_global_forwarding_rule.get("portRange")
        global_forwarding_rule_dict['target'] = raw_global_forwarding_rule.get("target")
        global_forwarding_rule_dict['load_balancing_scheme'] = raw_global_forwarding_rule.get("loadBalancingScheme")
        global_forwarding_rule_dict['network_tier'] = raw_global_forwarding_rule.get("networkTie")
        return global_forwarding_rule_dict['id'], global_forwarding_rule_dict