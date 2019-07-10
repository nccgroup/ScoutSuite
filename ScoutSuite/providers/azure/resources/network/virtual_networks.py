from ScoutSuite.providers.azure.resources.base import AzureResources


class VirtualNetworks(AzureResources):
    async def fetch_all(self):
        for raw_virtual_network in await self.facade.network.get_virtual_networks():
            id, virtual_network = self._parse_virtual_network(raw_virtual_network)
            self[id] = virtual_network

    def _parse_virtual_network(self, raw_virtual_network):
        virtual_network_dict = {}
        virtual_network_dict['subnets'] = raw_virtual_network.subnets
        virtual_network_dict['name'] = raw_virtual_network.name
        virtual_network_dict['tags'] = raw_virtual_network.tags
        virtual_network_dict['network_interfaces'] = raw_virtual_network.network_interfaces
        virtual_network_dict['resource_guid'] = raw_virtual_network.resource_guid
        virtual_network_dict['provisioning_state'] = raw_virtual_network.provisioning_state
        virtual_network_dict['etag'] = raw_virtual_network.etag
        virtual_network_dict['additional_properties'] = raw_virtual_network.additional_properties
        virtual_network_dict['location'] = raw_virtual_network.location
        virtual_network_dict['default_security_rules'] = raw_virtual_network.default_security_rules
        virtual_network_dict['security_rules'] = raw_virtual_network.security_rules
        virtual_network_dict['type'] = raw_virtual_network.type
        virtual_network_dict['id'] = raw_virtual_network.id
        return virtual_network_dict['id'], virtual_network_dict

