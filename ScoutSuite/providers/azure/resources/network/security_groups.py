from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class SecurityGroups(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(SecurityGroups, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_group in await self.facade.network.get_network_security_groups(self.subscription_id):
            id, network_security_group = self._parse_network_security_group(raw_group)
            self[id] = network_security_group

    def _parse_network_security_group(self, network_security_group):
        network_security_group_dict = {}
        network_security_group_dict['id'] = get_non_provider_id(network_security_group.id)
        network_security_group_dict['name'] = network_security_group.name
        network_security_group_dict['location'] = network_security_group.location
        network_security_group_dict['provisioning_state'] = network_security_group.provisioning_state
        network_security_group_dict['resource_guid'] = network_security_group.resource_guid
        network_security_group_dict['type'] = network_security_group.type
        network_security_group_dict['etag'] = network_security_group.etag
        network_security_group_dict['tags'] = network_security_group.tags
        network_security_group_dict['additional_properties'] = network_security_group.additional_properties

        network_security_group_dict['security_rules'] = self._parse_security_rules(network_security_group)

        network_security_group_dict['subnets'] = {}
        if network_security_group.subnets:
            for subnet in network_security_group.subnets:
                identifier = get_non_provider_id(subnet.id)
                network_security_group_dict['subnets'][identifier] = {'id': identifier}

        network_security_group_dict['network_interfaces'] = {}
        if network_security_group.network_interfaces:
            for network_interface in network_security_group.network_interfaces:
                identifier = get_non_provider_id(network_interface.id)
                network_security_group_dict['network_interfaces'][identifier] = {'id': identifier}

        # FIXME this is broken and badly implemented (not efficient at all)
        # exposed_ports = self._parse_exposed_ports(network_security_group)
        # network_security_group_dict['exposed_ports'] = exposed_ports
        # network_security_group_dict['exposed_port_ranges'] = self._format_ports(exposed_ports)

        return network_security_group_dict['id'], network_security_group_dict

    def _parse_security_rules(self, network_security_group):
        security_rules = {}
        # custom rules
        for sr in network_security_group.security_rules:
            security_rule_id, security_rule_dict = self._parse_security_rule(sr)
            security_rules[security_rule_id] = security_rule_dict
        # default rules
        for sr in network_security_group.default_security_rules:
            security_rule_id, security_rule_dict = self._parse_security_rule(sr, default=True)
            security_rules[security_rule_id] = security_rule_dict
        return security_rules

    def _parse_security_rule(self, rule, default=False):
        security_rule_dict = {}
        security_rule_dict['id'] = rule.id
        security_rule_dict['name'] = rule.name
        security_rule_dict['allow'] = rule.access == "Allow"
        security_rule_dict['priority'] = rule.priority
        security_rule_dict['description'] = rule.description
        security_rule_dict['provisioning_state'] = rule.provisioning_state

        security_rule_dict['protocol'] = rule.protocol
        security_rule_dict['direction'] = rule.direction

        source_address_prefixes = \
            self._merge_prefixes_or_ports(rule.source_address_prefix,
                                          rule.source_address_prefixes if rule.source_address_prefixes else
                                          (get_non_provider_id(rule.source_application_security_groups[0].id) if
                                           rule.source_application_security_groups else None))
        security_rule_dict['source_address_prefixes'] = source_address_prefixes
        # this is required for the HTML partial to interpret the source as an ASG
        if rule.source_application_security_groups:
            security_rule_dict['source_address_prefixes_is_asg'] = True
        else:
            security_rule_dict['source_address_prefixes_is_asg'] = False

        source_port_ranges = self._merge_prefixes_or_ports(rule.source_port_range, rule.source_port_ranges)
        security_rule_dict['source_port_ranges'] = source_port_ranges
        security_rule_dict['source_ports'] = self._parse_ports(source_port_ranges)

        destination_address_prefixes = self._merge_prefixes_or_ports(rule.destination_address_prefix,
                                                                     rule.destination_address_prefixes)
        security_rule_dict['destination_address_prefixes'] = destination_address_prefixes

        destination_port_ranges = self._merge_prefixes_or_ports(rule.destination_port_range,
                                                                rule.destination_port_ranges)
        security_rule_dict['destination_port_ranges'] = destination_port_ranges
        security_rule_dict['destination_ports'] = self._parse_ports(destination_port_ranges)

        security_rule_dict['etag'] = rule.etag

        security_rule_dict['default'] = default

        return security_rule_dict['id'], security_rule_dict

    def _parse_ports(self, port_ranges):
        # FIXME this is inefficient
        ports = set()
        for pr in port_ranges:
            if pr == "*":
                for p in range(0, 65535 + 1):
                    ports.add(p)
                break
            elif "-" in pr:
                lower, upper = pr.split("-")
                for p in range(int(lower), int(upper) + 1):
                    ports.add(p)
            else:
                ports.add(int(pr))
        ports = list(ports)
        ports.sort()
        return ports

    def _parse_exposed_ports(self, network_security_group):
        exposed_ports = set()

        # Sort by priority.
        rules = network_security_group.default_security_rules + network_security_group.security_rules
        rules.sort(key=lambda x: x.priority, reverse=True)

        for sr in rules:
            if sr.direction == "Inbound" and (sr.source_address_prefix == "*"
                                              or sr.source_address_prefix == "Internet"):
                port_ranges = self._merge_prefixes_or_ports(sr.destination_port_range,
                                                            sr.destination_port_ranges)
                ports = self._parse_ports(port_ranges)
                if sr.access == "Allow":
                    for p in ports:
                        exposed_ports.add(p)
                else:
                    for p in ports:
                        exposed_ports.discard(p)
        exposed_ports = list(exposed_ports)
        exposed_ports.sort()
        return exposed_ports

    def _merge_prefixes_or_ports(self, port_range, port_ranges):
        port_ranges = port_ranges if port_ranges else []
        if port_range:
            port_ranges.append(port_range)
        return port_ranges

    def _format_ports(self, ports):
        # FIXME this is inefficient
        port_ranges = []
        start = None
        for i in range(0, 65535 + 1):
            if i in ports:
                if not start:
                    start = i
            else:
                if start:
                    if i - 1 == start:
                        port_ranges.append(str(start))
                    else:
                        port_ranges.append(str(start) + "-" + str(i - 1))
                    start = None
        return port_ranges
