from ScoutSuite.providers.do.facade.base import DoFacade
from ScoutSuite.providers.do.resources.base import DoCompositeResources
from ScoutSuite.providers.do.resources.droplet.droplets import Droplets


class Droplets(DoCompositeResources):
    _children = [(Droplets, "droplets")]

    def __init__(self, facade: DoFacade):
        super().__init__(facade)
        self.service = "droplet"

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
