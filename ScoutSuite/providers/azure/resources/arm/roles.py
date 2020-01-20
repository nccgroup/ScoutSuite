from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class Roles(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(Roles, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_role in await self.facade.arm.get_roles(self.subscription_id):
            id, role = self._parse_role(raw_role)
            self[id] = role

    def _parse_role(self, raw_role):
        role_dict = {}
        role_dict['id'] = raw_role.name
        role_dict['name'] = raw_role.role_name
        role_dict['type'] = raw_role.type
        role_dict['description'] = raw_role.description
        role_dict['role_type'] = raw_role.role_type
        role_dict['permissions'] = raw_role.permissions
        role_dict['assignable_scopes'] = raw_role.assignable_scopes
        role_dict['additional_properties'] = raw_role.additional_properties
        role_dict['assignments_count'] = 0
        role_dict['assignments'] = {'users': [],
                                    'groups': [],
                                    'service_principals': []}  # this will be filled in `finalize()`
        return role_dict['id'], role_dict
