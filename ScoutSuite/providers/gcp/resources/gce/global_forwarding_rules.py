from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade


class GlobalForwardingRules(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_rules = await self.facade.gce.get_global_forwarding_rules(self.project_id)
        for raw_rule in raw_rules:
            rule_id, rule = self._parse_forwarding_rule(raw_rule)
            self[rule_id] = rule

    def _parse_forwarding_rule(self, raw_global_forwarding_rule):
        global_forwarding_rule_dict = {}
        global_forwarding_rule_dict['id'] = raw_global_forwarding_rule.get("id")
        global_forwarding_rule_dict['name'] = raw_global_forwarding_rule.get("name")
        global_forwarding_rule_dict['creation_timestamp'] = raw_global_forwarding_rule.get("creationTimestamp")
        global_forwarding_rule_dict['description'] = raw_global_forwarding_rule.get("description")
        global_forwarding_rule_dict['ip_address'] = raw_global_forwarding_rule.get("IPAddress")
        global_forwarding_rule_dict['ip_protocol'] = raw_global_forwarding_rule.get("IPProtocol")
        global_forwarding_rule_dict['all_ports'] = raw_global_forwarding_rule.get("allPorts", False)
        global_forwarding_rule_dict['port_range'] = raw_global_forwarding_rule.get("portRange", "")
        global_forwarding_rule_dict['ports'] = raw_global_forwarding_rule.get("ports", [])
        global_forwarding_rule_dict['target'] = raw_global_forwarding_rule.get("target")
        global_forwarding_rule_dict['load_balancing_scheme'] = raw_global_forwarding_rule.get("loadBalancingScheme")
        global_forwarding_rule_dict['network_tier'] = raw_global_forwarding_rule.get("networkTie")

        global_forwarding_rule_dict['subnetwork'] = raw_global_forwarding_rule.get("subnetwork")
        global_forwarding_rule_dict['network'] = raw_global_forwarding_rule.get("network")
        global_forwarding_rule_dict['backend_service'] = raw_global_forwarding_rule.get("backendService")
        global_forwarding_rule_dict['service_label'] = raw_global_forwarding_rule.get("serviceLabel")
        global_forwarding_rule_dict['service_name'] = raw_global_forwarding_rule.get("serviceName")
        global_forwarding_rule_dict['labels'] = raw_global_forwarding_rule.get("labels")
        global_forwarding_rule_dict['ip_version'] = raw_global_forwarding_rule.get("ipVersion")
        global_forwarding_rule_dict['allow_global_access'] = raw_global_forwarding_rule.get("allowGlobalAccess")

        return global_forwarding_rule_dict['id'], global_forwarding_rule_dict