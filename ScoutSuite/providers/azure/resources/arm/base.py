from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .roles import Roles
from .role_assignments import RoleAssignments


class ARM(AzureCompositeResources):
    _children = [
        (Roles, 'roles'),
        (RoleAssignments, 'role_assignments')

    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)


