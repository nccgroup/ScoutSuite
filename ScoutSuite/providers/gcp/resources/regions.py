from ScoutSuite.providers.gcp.facade.base import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources


class Regions(GCPCompositeResources):
    def __init__(self, facade: GCPFacade, project_id: str):
        super(Regions, self).__init__(facade)
        self.project_id = project_id

    async def fetch_all(self):
        raw_regions = await self.facade.gce.get_regions(self.project_id)
        for raw_region in raw_regions:
            self[raw_region['name']] = {}
        await self._fetch_children_of_all_resources(
            resources=self,
            scopes={region: {'project_id': self.project_id, 'region': region} for region in self})
