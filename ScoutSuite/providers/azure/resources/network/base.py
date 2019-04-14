from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .network_security_groups import NetworkSecurityGroups
from .network_watchers import NetworkWatchers


class Networks(AzureCompositeResources):
    _children = [
        (NetworkSecurityGroups, 'network_security_groups'),
        (NetworkWatchers, 'network_watchers')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
