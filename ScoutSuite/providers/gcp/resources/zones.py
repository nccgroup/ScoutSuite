from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources


class Zones(GCPCompositeResources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super().__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_zones = await self.facade.gce.get_zones(self.project_id)
        for raw_zone in raw_zones:
            self[raw_zone['name']] = {}
        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={zone: {'project_id': self.project_id, 'zone': zone} for zone in self})
