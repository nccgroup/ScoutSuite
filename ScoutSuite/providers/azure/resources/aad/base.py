from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .users import Users
from .groups import Groups
from .serviceprincipals import ServicePrincipals
from .applications import Applications


class AAD(AzureCompositeResources):
    _children = [
        (Users, 'users'),
        (Groups, 'groups'),
        (ServicePrincipals, 'service_principals'),
        (Applications, 'applications'),
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)

    async def finalize(self):

        # Add group members
        for group in self['groups']:
            for user in self['users']:
                if group in self['users'][user]['groups']:
                    self['groups'][group]['users'].append(user)
