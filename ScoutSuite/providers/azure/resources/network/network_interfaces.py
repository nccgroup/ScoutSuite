from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class NetworkInterfaces(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(NetworkInterfaces, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_network_interface in await self.facade.network.get_network_interfaces(self.subscription_id):
            id, network_interface = self._parse_network_interface(raw_network_interface)
            self[id] = network_interface

    def _parse_network_interface(self, raw_network_interface):
        network_interface_dict = {}
        network_interface_dict['id'] = get_non_provider_id(raw_network_interface.id)
        network_interface_dict['enable_accelerated_networking'] = raw_network_interface.enable_accelerated_networking
        network_interface_dict['virtual_machine'] = \
            get_non_provider_id(raw_network_interface.virtual_machine.id.lower()) if \
                raw_network_interface.virtual_machine else None
        network_interface_dict['name'] = raw_network_interface.name
        network_interface_dict['tags'] = raw_network_interface.tags
        network_interface_dict['interface_endpoint'] = raw_network_interface.interface_endpoint if \
            hasattr(raw_network_interface, 'interface_endpoint') else None
        network_interface_dict['primary'] = raw_network_interface.primary
        network_interface_dict['etag'] = raw_network_interface.etag
        network_interface_dict['additional_properties'] = raw_network_interface.additional_properties
        network_interface_dict['location'] = raw_network_interface.location
        network_interface_dict['mac_address'] = raw_network_interface.mac_address
        network_interface_dict['provisioning_state'] = raw_network_interface.provisioning_state
        network_interface_dict['resource_guid'] = raw_network_interface.resource_guid
        network_interface_dict['enable_ip_forwarding'] = raw_network_interface.enable_ip_forwarding
        network_interface_dict['type'] = raw_network_interface.type
        network_interface_dict['network_security_group'] = \
            get_non_provider_id(raw_network_interface.network_security_group.id) if \
                raw_network_interface.network_security_group else None

        # TODO process and display the below
        network_interface_dict['hosted_workloads'] = raw_network_interface.hosted_workloads
        network_interface_dict['tap_configurations'] = raw_network_interface.tap_configurations
        network_interface_dict['dns_settings'] = raw_network_interface.dns_settings

        ip_configuration = raw_network_interface.ip_configurations[0]  # TODO is this always an array of 1?
        network_interface_dict['ip_configuration'] = {}
        network_interface_dict['ip_configuration']['id'] = ip_configuration.id
        network_interface_dict['ip_configuration']['additional_properties'] = ip_configuration.additional_properties
        network_interface_dict['ip_configuration']['virtual_network_taps'] = ip_configuration.virtual_network_taps
        network_interface_dict['ip_configuration'][
            'application_gateway_backend_address_pools'] = ip_configuration.application_gateway_backend_address_pools
        network_interface_dict['ip_configuration'][
            'load_balancer_backend_address_pools'] = ip_configuration.load_balancer_backend_address_pools
        network_interface_dict['ip_configuration'][
            'load_balancer_inbound_nat_rules'] = ip_configuration.load_balancer_inbound_nat_rules
        network_interface_dict['ip_configuration']['private_ip_address'] = ip_configuration.private_ip_address
        network_interface_dict['ip_configuration'][
            'private_ip_allocation_method'] = ip_configuration.private_ip_allocation_method
        network_interface_dict['ip_configuration'][
            'private_ip_address_version'] = ip_configuration.private_ip_address_version
        network_interface_dict['ip_configuration']['subnet'] = {'id': get_non_provider_id(ip_configuration.subnet.id)}
        network_interface_dict['ip_configuration']['primary'] = ip_configuration.primary
        network_interface_dict['ip_configuration']['public_ip_address'] = ip_configuration.public_ip_address
        network_interface_dict['ip_configuration']['provisioning_state'] = ip_configuration.provisioning_state
        network_interface_dict['ip_configuration']['name'] = ip_configuration.name
        network_interface_dict['ip_configuration']['etag'] = ip_configuration.etag

        network_interface_dict['ip_configuration']['application_security_groups'] = []
        if ip_configuration.application_security_groups:
            for asg in ip_configuration.application_security_groups:
                network_interface_dict['ip_configuration']['application_security_groups'].append(
                    get_non_provider_id(asg.id))

        # FIXME this is currently always None, might change in the future?
        # network_interface_dict['ip_configuration']['subnet_security_group'] = ip_configuration.subnet.network_security_group

        return network_interface_dict['id'], network_interface_dict
