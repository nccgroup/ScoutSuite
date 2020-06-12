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

    async def fetch_additional_users(self, user_list):
        """
        Special method to fetch additional users
        """
        # fetch the users
        additional_users = Users(self.facade)
        await additional_users.fetch_additional_users(user_list)
        # add them to the resource and update count
        self['users'].update(additional_users)
        self['users_count'] = len(self['users'].values())
        # re-run the finalize method
        await self.finalize()

    async def finalize(self):
        self.assign_group_memberships()

    def assign_group_memberships(self):
        """
        Assigns members to groups
        """
        for group in self['groups']:
            for user in self['users']:
                if group in self['users'][user]['groups']:
                    self['groups'][group]['users'].append(user)
