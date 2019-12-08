from ScoutSuite.providers.azure.resources.base import AzureCompositeResources

from .users import Users
from .groups import Groups
from .serviceprincipals import ServicePrincipals
from .applications import Applications
from .roles import Roles


class GraphRBAC(AzureCompositeResources):
    _children = [
        (Users, 'users'),
        (Groups, 'groups'),
        (ServicePrincipals, 'service_principals'),
        (Applications, 'applications'),
        (Roles, 'roles')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)

    async def finalize(self):

        # Add group members
        for group in self['groups']:
            for user in self['users']:
                if group in self['users'][user]['groups']:
                    self['groups'][group]['users'].append(user)

        # Add role assignments
        assignments = await self.facade.graphrbac.get_role_assignments()
        for assignment in assignments:
            role_id = assignment.role_definition_id.split('/')[-1]
            for group in self['groups']:
                if group == assignment.principal_id:
                    self['groups'][group]['roles'].append(role_id)
                    self['roles'][role_id]['assignments']['groups'].append(group)
                    self['roles'][role_id]['assignments_count'] += 1
            for user in self['users']:
                if user == assignment.principal_id:
                    self['users'][user]['roles'].append(role_id)
                    self['roles'][role_id]['assignments']['users'].append(user)
                    self['roles'][role_id]['assignments_count'] += 1
            for service_principal in self['service_principals']:
                if service_principal == assignment.principal_id:
                    self['service_principals'][service_principal]['roles'].append(role_id)
                    self['roles'][role_id]['assignments']['service_principals'].append(service_principal)
                    self['roles'][role_id]['assignments_count'] += 1
