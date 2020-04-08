from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources


class RoleAssignments(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super(RoleAssignments, self).__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_role_assignment in await self.facade.arm.get_role_assignments(self.subscription_id):
            id, role_assignment = self._parse_role_assignment(raw_role_assignment)
            self[id] = role_assignment

    def _parse_role_assignment(self, raw_role_assignment):
        role_assignment_dict = {}
        role_assignment_dict['id'] = raw_role_assignment.name
        role_assignment_dict['name'] = raw_role_assignment.name
        role_assignment_dict['role_definition_id'] = raw_role_assignment.role_definition_id
        role_assignment_dict['type'] = raw_role_assignment.type
        role_assignment_dict['scope'] = raw_role_assignment.scope
        role_assignment_dict['principal_id'] = raw_role_assignment.principal_id
        role_assignment_dict['principal_type'] = raw_role_assignment.principal_type
        role_assignment_dict['can_delegate'] = raw_role_assignment.can_delegate
        role_assignment_dict['additional_properties'] = raw_role_assignment.additional_properties
        return role_assignment_dict['id'], role_assignment_dict
