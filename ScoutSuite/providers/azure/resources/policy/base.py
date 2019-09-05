from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .policy_assignments import PolicyAssignments

class Policies(AzureCompositeResources):
    _children = [
        (PolicyAssignments, 'policy_assignments'),
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)