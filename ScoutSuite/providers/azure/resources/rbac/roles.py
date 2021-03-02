from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class Roles(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_role in await self.facade.rbac.get_roles(self.subscription_id):
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
        role_dict['custom_subscription_owner_role'] = self._no_custom_subscription_owner_role_allowed(raw_role)
        role_dict['assignments'] = {'users': [],
                                    'groups': [],
                                    'service_principals': []}  # this will be filled in `finalize()`
        return role_dict['id'], role_dict

    def _no_custom_subscription_owner_role_allowed(self, role):
        if role.role_type =="CustomRole":
            for assignable_scope in role.assignable_scopes:
                if "subscriptions" in assignable_scope or assignable_scope == "/":
                    for permission in role.permissions:
                        for action in permission.actions:
                            if "*" in action:
                                return True
        return False

