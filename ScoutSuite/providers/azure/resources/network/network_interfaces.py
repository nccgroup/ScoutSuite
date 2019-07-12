from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class NetworkInterfaces(AzureResources):
    async def fetch_all(self):
        for raw_network_interface in await self.facade.network.get_network_interfaces():
            id, network_interface = self._parse_network_interface(raw_network_interface)
            self[id] = network_interface

    def _parse_network_interface(self, raw_network_interface):
        network_interface_dict = {}
        network_interface_dict['id'] = get_non_provider_id(raw_network_interface.id)
        network_interface_dict['enable_accelerated_networking'] = raw_network_interface.enable_accelerated_networking
        network_interface_dict['dns_settings'] = raw_network_interface.dns_settings
        network_interface_dict['virtual_machine'] = raw_network_interface.virtual_machine
        network_interface_dict['name'] = raw_network_interface.name
        network_interface_dict['tags'] = raw_network_interface.tags
        network_interface_dict['interface_endpoint'] = raw_network_interface.interface_endpoint
        network_interface_dict['primary'] = raw_network_interface.primary
        network_interface_dict['tap_configurations'] = raw_network_interface.tap_configurations
        network_interface_dict['etag'] = raw_network_interface.etag
        network_interface_dict['additional_properties'] = raw_network_interface.additional_properties
        network_interface_dict['location'] = raw_network_interface.location
        network_interface_dict['mac_address'] = raw_network_interface.mac_address
        network_interface_dict['provisioning_state'] = raw_network_interface.provisioning_state
        network_interface_dict['resource_guid'] = raw_network_interface.resource_guid
        network_interface_dict['ip_configurations'] = raw_network_interface.ip_configurations
        network_interface_dict['enable_ip_forwarding'] = raw_network_interface.enable_ip_forwarding
        network_interface_dict['type'] = raw_network_interface.type
        network_interface_dict['hosted_workloads'] = raw_network_interface.hosted_workloads
        network_interface_dict['network_security_group'] = raw_network_interface.network_security_group
        return network_interface_dict['id'], network_interface_dict

