from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .users import Users


class GraphRBAC(AzureCompositeResources):
    _children = [
        (Users, 'users'),
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)
