import asyncio
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.resources import GCPCompositeResources

class Regions(GCPCompositeResources):
    def __init__(self, gcp_facade: GCPFacade, project_id: str):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_regions = await self.gcp_facade.gce.get_regions(self.project_id)
        for raw_region in raw_regions:
            self[raw_region['name']] = {}
        tasks = {
            asyncio.ensure_future(
                self._fetch_children(self[raw_region['name']], gcp_facade = self.gcp_facade, project_id = self.project_id, region = raw_region['name'])
            ) for raw_region in raw_regions
        }
        await asyncio.wait(tasks)
