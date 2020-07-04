from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id
from ScoutSuite.providers.azure.utils import get_resource_group_name


class VirtualNetworks(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_virtual_network in await self.facade.network.get_virtual_networks(self.subscription_id):
            id, virtual_network = self._parse_virtual_network(raw_virtual_network)
            self[id] = virtual_network

    def _parse_virtual_network(self, raw_virtual_network):
        virtual_network_dict = {}
        virtual_network_dict['id'] = get_non_provider_id(raw_virtual_network.id)
        virtual_network_dict['name'] = raw_virtual_network.name

        virtual_network_dict['enable_vm_protection'] = raw_virtual_network.enable_vm_protection
        virtual_network_dict['etag'] = str(raw_virtual_network.etag)
        if raw_virtual_network.tags is not None:
            virtual_network_dict['tags'] = ["{}:{}".format(key, value) for key, value in  raw_virtual_network.tags.items()]
        else:
            virtual_network_dict['tags'] = []
        virtual_network_dict['resource_group_name'] = get_resource_group_name(raw_virtual_network.id)
        virtual_network_dict['virtual_network_peerings'] = raw_virtual_network.virtual_network_peerings
        virtual_network_dict['enable_ddos_protection'] = raw_virtual_network.enable_ddos_protection
        virtual_network_dict['resource_guid'] = raw_virtual_network.resource_guid
        virtual_network_dict['provisioning_state'] = raw_virtual_network.provisioning_state
        virtual_network_dict['address_space'] = raw_virtual_network.address_space
        virtual_network_dict['ddos_protection_plan'] = raw_virtual_network.ddos_protection_plan
        virtual_network_dict['additional_properties'] = list(raw_virtual_network.additional_properties)
        virtual_network_dict['location'] = raw_virtual_network.location
        virtual_network_dict['type'] = raw_virtual_network.type
        virtual_network_dict['dhcp_options'] = raw_virtual_network.dhcp_options

        virtual_network_dict['subnets'] = {}
        virtual_network_dict['subnets_count'] = 0
        for raw_subnet in raw_virtual_network.subnets:
            subnet_dict = {}
            subnet_dict['id'] = get_non_provider_id(raw_subnet.id)
            subnet_dict['name'] = raw_subnet.name
            subnet_dict['service_association_links'] = raw_subnet.service_association_links
            subnet_dict['resource_navigation_links'] = raw_subnet.resource_navigation_links
            subnet_dict['service_endpoint_policies'] = raw_subnet.service_endpoint_policies
            subnet_dict['interface_endpoints'] = raw_subnet.interface_endpoints if \
                hasattr(raw_subnet, 'interface_endpoints') else None
            subnet_dict['purpose'] = raw_subnet.purpose
            subnet_dict['address_prefix'] = raw_subnet.address_prefix
            subnet_dict['provisioning_state'] = raw_subnet.provisioning_state
            subnet_dict['etag'] = str(raw_subnet.etag)
            subnet_dict['additional_properties'] = raw_subnet.additional_properties
            subnet_dict['route_table'] = raw_subnet.route_table
            subnet_dict['delegations'] = raw_subnet.delegations
            subnet_dict['service_endpoints'] = raw_subnet.service_endpoints
            subnet_dict['ip_configuration_profiles'] = raw_subnet.ip_configuration_profiles
            subnet_dict['ip_configurations'] = raw_subnet.ip_configurations
            subnet_dict['address_prefixes'] = raw_subnet.address_prefixes
            if raw_subnet.network_security_group:
                subnet_dict['network_security_group'] = get_non_provider_id(raw_subnet.network_security_group.id)
            else:
                subnet_dict['network_security_group'] = None
            virtual_network_dict['subnets_count'] += 1
            virtual_network_dict['subnets'][subnet_dict['id']] = subnet_dict

        return virtual_network_dict['id'], virtual_network_dict
