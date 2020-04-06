from ScoutSuite.providers.azure.resources.subscriptions import Subscriptions
from .application_security_groups import ApplicationSecurityGroups
from .network_interfaces import NetworkInterfaces
from .security_groups import SecurityGroups
from .virtual_networks import VirtualNetworks
from .watchers import Watchers


class Networks(Subscriptions):
    _children = [
        (VirtualNetworks, 'virtual_networks'),
        (SecurityGroups, 'security_groups'),
        (ApplicationSecurityGroups, 'application_security_groups'),
        (NetworkInterfaces, 'network_interfaces'),
        (Watchers, 'watchers')
    ]

    async def finalize(self):
        await self._match_subnets_and_security_groups()
        await self._match_subnets_and_network_interfaces()
        await self._match_asgs_and_network_interfaces()

    async def _match_subnets_and_security_groups(self):
        """
        Goes through each security groups' subnets and adds the ID of the subnet's virtual network.
        This is useful in the partials as both the subnet and its network's IDs are needed to build the path.
        """
        for subscription in self['subscriptions']:
            for sg in self['subscriptions'][subscription]['security_groups']:
                for subnet in self['subscriptions'][subscription]['security_groups'][sg]['subnets']:
                    for network in self['subscriptions'][subscription]['virtual_networks']:
                        for network_subnet in self['subscriptions'][subscription]['virtual_networks'][network].get('subnets', []):
                            if subnet == network_subnet:
                                self['subscriptions'][subscription]['security_groups'][sg]['subnets'][subnet]['virtual_network_id'] = network

    async def _match_subnets_and_network_interfaces(self):
        """
        Goes through each security groups' subnets and adds the network interfaces and instances that are placed in it.
        """
        for subscription in self['subscriptions']:
            for interface in self['subscriptions'][subscription]['network_interfaces']:
                subnet_id = self['subscriptions'][subscription]['network_interfaces'][interface]['ip_configuration']['subnet']['id']
                for network in self['subscriptions'][subscription]['virtual_networks']:
                    for network_subnet in self['subscriptions'][subscription]['virtual_networks'][network].get('subnets', []):
                        if not 'instances' in self['subscriptions'][subscription]['virtual_networks'][network]['subnets'][network_subnet]:
                            self['subscriptions'][subscription]['virtual_networks'][network]['subnets'][network_subnet]['instances'] = []
                        if subnet_id == network_subnet:
                            self['subscriptions'][subscription]['network_interfaces'][interface]['ip_configuration']['subnet'][
                                'virtual_network_id'] = network
                            self['subscriptions'][subscription]['virtual_networks'][network]['subnets'][network_subnet]['instances'].append(
                                self['subscriptions'][subscription]['network_interfaces'][interface]['virtual_machine'])

    async def _match_asgs_and_network_interfaces(self):
        """
        Goes through each application security group and add the network interfaces and instances that are placed in it.
        """
        for subscription in self['subscriptions']:
            for interface in self['subscriptions'][subscription]['network_interfaces']:
                for asg in self['subscriptions'][subscription]['network_interfaces'][interface]['ip_configuration']['application_security_groups']:
                    self['subscriptions'][subscription]['application_security_groups'][asg]['network_interfaces'].append(interface)
