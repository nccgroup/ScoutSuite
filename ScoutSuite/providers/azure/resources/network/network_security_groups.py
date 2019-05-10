from ScoutSuite.providers.azure.resources.base import AzureResources


class NetworkSecurityGroups(AzureResources):
    async def fetch_all(self):
        for raw_group in await self.facade.network.get_network_security_groups():
            id, network_security_group = self._parse_network_security_group(raw_group)
            self[id] = network_security_group

    def _parse_network_security_group(self, network_security_group):
        network_security_group_dict = {}
        network_security_group_dict['id'] = network_security_group.resource_guid
        network_security_group_dict['name'] = network_security_group.name
        network_security_group_dict['provisioning_state'] = network_security_group.provisioning_state
        network_security_group_dict['location'] = network_security_group.location
        network_security_group_dict['resource_guid'] = network_security_group.resource_guid
        network_security_group_dict['etag'] = network_security_group.etag

        network_security_group_dict['security_rules'] = self._parse_security_rules(network_security_group)

        # FIXME this is broken and badly implemented (not efficient at all)
        # exposed_ports = self._parse_exposed_ports(network_security_group)
        # network_security_group_dict['exposed_ports'] = exposed_ports
        # network_security_group_dict['exposed_port_ranges'] = self._format_ports(exposed_ports)

        return network_security_group_dict['id'], network_security_group_dict

    def _parse_security_rules(self, network_security_group):
        security_rules = {}
        for sr in network_security_group.security_rules:
            security_rule_dict = {}
            security_rule_dict['id'] = sr.id
            security_rule_dict['name'] = sr.name
            security_rule_dict['allow'] = sr.access == "Allow"
            security_rule_dict['priority'] = sr.priority
            security_rule_dict['description'] = sr.description
            security_rule_dict['provisioning_state'] = sr.provisioning_state

            security_rule_dict['protocol'] = sr.protocol
            security_rule_dict['direction'] = sr.direction

            source_address_prefixes = self._merge_prefixes_or_ports(sr.source_address_prefix,
                                                                    sr.source_address_prefixes)
            security_rule_dict['source_address_prefixes'] = source_address_prefixes

            source_port_ranges = self._merge_prefixes_or_ports(sr.source_port_range, sr.source_port_ranges)
            security_rule_dict['source_port_ranges'] = source_port_ranges
            security_rule_dict['source_ports'] = self._parse_ports(source_port_ranges)

            destination_address_prefixes = self._merge_prefixes_or_ports(sr.destination_address_prefix,
                                                                         sr.destination_address_prefixes)
            security_rule_dict['destination_address_prefixes'] = destination_address_prefixes

            destination_port_ranges = self._merge_prefixes_or_ports(sr.destination_port_range,
                                                                    sr.destination_port_ranges)
            security_rule_dict['destination_port_ranges'] = destination_port_ranges
            security_rule_dict['destination_ports'] = self._parse_ports(destination_port_ranges)

            security_rule_dict['etag'] = sr.etag

            security_rules[security_rule_dict['id']] = security_rule_dict

        return security_rules

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

