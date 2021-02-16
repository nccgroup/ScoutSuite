from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.core.console import print_exception


class ServiceAccountBindings(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, service_account_email: str):
        super().__init__(facade)
        self.project_id = project_id
        self.service_account_email = service_account_email 

    async def fetch_all(self):
        raw_bindings = await self.facade.iam.get_service_account_bindings(self.project_id, self.service_account_email)
        parsing_error_counter = 0
        for raw_binding in raw_bindings:
            try:
                binding_id, binding = self._parse_binding(raw_binding)
                self[binding_id] = binding
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_binding(self, raw_binding):
        return len(self), raw_binding
