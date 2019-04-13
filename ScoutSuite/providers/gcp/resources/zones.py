import asyncio
from ScoutSuite.providers.gcp.facade.gcp import GCPFacade
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources


class Zones(GCPCompositeResources):
    def __init__(self, gcp_facade: GCPFacade, project_id: str):
        self.gcp_facade = gcp_facade
        self.project_id = project_id

    async def fetch_all(self):
        raw_zones = await self.gcp_facade.gce.get_zones(self.project_id)
        for raw_zone in raw_zones:
            self[raw_zone['name']] = {}
        tasks = {
            asyncio.ensure_future(
                self._fetch_children(self[raw_zone['name']], scope={
                                     'gcp_facade': self.gcp_facade, 'project_id': self.project_id, 'zone': raw_zone['name']})
            ) for raw_zone in raw_zones
        }
        await asyncio.wait(tasks)
