# -*- coding: utf-8 -*-

from ScoutSuite.providers.azure.configs.base import AzureBaseConfig


class NetworkConfig(AzureBaseConfig):
    targets = (
        ('network_security_groups', 'Network Security Group', 'list_all', {}, False),
    )

    def __init__(self, thread_config):
        self.network_security_groups = {}
        self.network_security_groups_count = 0

        super(NetworkConfig, self).__init__(thread_config)

    def parse_network_security_groups(self, network_security_group, params):
        network_security_group_dict = {}
        network_security_group_dict['id'] = network_security_group.id
        network_security_group_dict['name'] = network_security_group.name
        network_security_group_dict['provisioning_state'] = network_security_group.provisioning_state
        network_security_group_dict['location'] = network_security_group.location
        network_security_group_dict['resource_guid'] = network_security_group.resource_guid
        network_security_group_dict['etag'] = network_security_group.etag

        network_security_group_dict['security_rules'] = self._parse_security_rules(network_security_group)

        self.network_security_groups[network_security_group_dict['id']] = network_security_group_dict

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
            security_rule_dict['source_address_prefix'] = sr.source_address_prefix
            security_rule_dict['source_ports'] = self._parse_ports(sr.source_port_range, sr.source_port_ranges)
            security_rule_dict['destination_address_prefix '] = sr.destination_address_prefix
            security_rule_dict['destination_ports'] = self._parse_ports(sr.destination_port_range,
                                                                        sr.destination_port_ranges)

            security_rule_dict['etag'] = sr.etag

            security_rules[security_rule_dict['id']] = security_rule_dict

        return security_rules

    def _parse_ports(self, port_range, port_ranges):
        ports = set()
        port_ranges.append(ports)
        for pr in port_ranges:
            # Get all port from the port range
            pass
        return ports