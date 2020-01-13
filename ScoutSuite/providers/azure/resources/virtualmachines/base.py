from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .instances import Instances


class VirtualMachines(AzureCompositeResources):
    _children = [
        (Instances, 'instances')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
