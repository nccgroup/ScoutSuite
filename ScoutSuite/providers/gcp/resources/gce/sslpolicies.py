from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class SSLPolicies(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_policies = await self.facade.gce.get_sslpolicies(self.project_id)
        for raw_policy in raw_policies:
            self[get_non_provider_id(raw_policy.get('id'))] = raw_policy
