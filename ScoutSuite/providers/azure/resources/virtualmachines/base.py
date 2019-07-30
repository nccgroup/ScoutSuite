from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.providers.azure.utils import get_resource_group_name
from ScoutSuite.providers.utils import get_non_provider_id

from .instances import Instances

class VirtualMachines(AzureCompositeResources):
    _children = [
        (Instances, 'instances')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
