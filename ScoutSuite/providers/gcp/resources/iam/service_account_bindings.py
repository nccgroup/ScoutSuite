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
        for raw_binding in raw_bindings:
            try:
                binding_id, binding = self._parse_binding(raw_binding)
                self[binding_id] = binding
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_binding(self, raw_binding):
        return len(self), raw_binding
