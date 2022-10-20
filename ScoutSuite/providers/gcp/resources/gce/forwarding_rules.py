from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class ForwardingRules(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, region: str):
        super().__init__(facade)
        self.project_id = project_id
        self.region = region

    async def fetch_all(self):
        raw_rules = await self.facade.gce.get_forwarding_rules(self.project_id, self.region)
        for raw_rule in raw_rules:
            try:
                rule_id, rule = self._parse_forwarding_rule(raw_rule)
            except Exception as e:
                print(e)
            self[rule_id] = rule

    def _parse_forwarding_rule(self, raw_forwarding_rule):
        forwarding_rule_dict = {}
        forwarding_rule_dict['id'] = raw_forwarding_rule.get("id")
        forwarding_rule_dict['name'] = raw_forwarding_rule.get("name")
        forwarding_rule_dict['creation_timestamp'] = raw_forwarding_rule.get("creationTimestamp")
        forwarding_rule_dict['description'] = raw_forwarding_rule.get("description")
        forwarding_rule_dict['region'] = raw_forwarding_rule.get("region")
        forwarding_rule_dict['ip_address'] = raw_forwarding_rule.get("IPAddress")
        forwarding_rule_dict['ip_protocol'] = raw_forwarding_rule.get("IPProtocol")
        forwarding_rule_dict['port_range'] = raw_forwarding_rule.get("portRange")
        forwarding_rule_dict['target'] = raw_forwarding_rule.get("target")
        forwarding_rule_dict['load_balancing_scheme'] = raw_forwarding_rule.get("loadBalancingScheme")
        forwarding_rule_dict['network_tier'] = raw_forwarding_rule.get("networkTier")
        return forwarding_rule_dict['id'], forwarding_rule_dict