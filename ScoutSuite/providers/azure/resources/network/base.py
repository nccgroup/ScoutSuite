from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .virtual_networks import VirtualNetworks
from .security_groups import SecurityGroups
from .network_interfaces import NetworkInterfaces
from .watchers import Watchers


class Networks(AzureCompositeResources):
    _children = [
        (VirtualNetworks, 'virtual_networks'),
        (SecurityGroups, 'security_groups'),
        (NetworkInterfaces, 'network_interfaces'),
        (Watchers, 'watchers')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)


    async def finalize(self):
        await self._match_subnets_and_security_groups()
        await self._match_subnets_and_network_interfaces()

    async def _match_subnets_and_security_groups(self):
        """
        Goes through each security groups' subnets and adds the ID of the subnet's virtual network.
        This is useful in the partials as both the subnet and its network's IDs are needed to build the path.
        """
        for sg in self['security_groups']:
            for subnet in self['security_groups'][sg]['subnets']:
                for network in self['virtual_networks']:
                    for network_subnet in self['virtual_networks'][network].get('subnets', []):
                        if subnet == network_subnet:
                            self['security_groups'][sg]['subnets'][subnet]['virtual_network_id'] = network

    async def _match_subnets_and_network_interfaces(self):
        """
        Goes through each security groups' subnets and adds the network interfaces and instances that are placed in it.
        """
        for interface in self['network_interfaces']:
            subnet_id = self['network_interfaces'][interface]['ip_configuration']['subnet']['id']
            for network in self['virtual_networks']:
                for network_subnet in self['virtual_networks'][network].get('subnets', []):
                    if not 'instances' in self['virtual_networks'][network]['subnets'][network_subnet]:
                        self['virtual_networks'][network]['subnets'][network_subnet]['instances'] = []
                    if subnet_id == network_subnet:
                        self['network_interfaces'][interface]['ip_configuration']['subnet']['virtual_network_id'] = network
                        self['virtual_networks'][network]['subnets'][network_subnet]['instances'].append(self['network_interfaces'][interface]['virtual_machine'])
