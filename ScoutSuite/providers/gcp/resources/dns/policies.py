from ScoutSuite.providers.base.resources.base import Resources
from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.utils import get_non_provider_id


class Policies(Resources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_policies = await self.facade.dns.get_policies(self.project_id)
        for raw_policy in raw_policies.get('policies', []):
            self[get_non_provider_id(raw_policy.get('name'))] = raw_policy
