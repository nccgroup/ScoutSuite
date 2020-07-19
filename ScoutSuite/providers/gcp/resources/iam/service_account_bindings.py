from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.base.resources.base import Resources


class ServiceAccountBindings(Resources):
    def __init__(self, facade: GCPFacade, project_id: str, service_account_email: str):
        super().__init__(facade)
        self.project_id = project_id
        self.service_account_email = service_account_email 

    async def fetch_all(self):
        raw_bindings = await self.facade.iam.get_service_account_bindings(self.project_id, self.service_account_email)
        for raw_binding in raw_bindings:
            binding_id, binding = self._parse_binding(raw_binding)
            self[binding_id] = binding

    def _parse_binding(self, raw_binding):
        return len(self), raw_binding
