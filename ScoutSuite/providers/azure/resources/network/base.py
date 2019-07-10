from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .virtual_networks import VirtualNetworks
from .security_groups import SecurityGroups
from .watchers import Watchers


class Networks(AzureCompositeResources):
    _children = [
        (VirtualNetworks, 'virtual_networks'),
        (SecurityGroups, 'security_groups'),
        (Watchers, 'watchers')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
