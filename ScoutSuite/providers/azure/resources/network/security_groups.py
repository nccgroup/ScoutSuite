from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.utils import get_resource_group_name


class SecurityGroups(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
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
        if network_security_group.tags is not None:
            network_security_group_dict['tags'] = ["{}:{}".format(key, value) for key, value in  network_security_group.tags.items()]
        else:
            network_security_group_dict['tags'] = []
        network_security_group_dict['resource_group_name'] = get_resource_group_name(network_security_group.id)
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

        security_rule_dict['source_port_ranges'] = self._merge_prefixes_or_ports(rule.source_port_range, rule.source_port_ranges)
        security_rule_dict['source_ports'] = ['0-65535'] if '*' in security_rule_dict['source_port_ranges'] else security_rule_dict['source_port_ranges']

        security_rule_dict['destination_address_prefixes'] = self._merge_prefixes_or_ports(rule.destination_address_prefix, rule.destination_address_prefixes)

        security_rule_dict['destination_port_ranges'] = self._merge_prefixes_or_ports(rule.destination_port_range, rule.destination_port_ranges)
        security_rule_dict['destination_ports'] = ['0-65535'] if '*' in security_rule_dict['destination_port_ranges'] else security_rule_dict['destination_port_ranges']

        security_rule_dict['etag'] = rule.etag

        security_rule_dict['default'] = default

        return security_rule_dict['id'], security_rule_dict

    def _merge_prefixes_or_ports(self, port_range, port_ranges):
        port_ranges = port_ranges if port_ranges else []
        if port_range:
            port_ranges.append(port_range)
        return port_ranges
