from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class RoleAssignments(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        parsing_error_counter = 0
        for raw_role_assignment in await self.facade.rbac.get_role_assignments(self.subscription_id):
            try:
                id, role_assignment = self._parse_role_assignment(raw_role_assignment)
                self[id] = role_assignment
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

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
