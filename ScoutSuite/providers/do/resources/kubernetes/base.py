from ScoutSuite.providers.do.facade.base import DoFacade
from ScoutSuite.providers.do.resources.base import DoCompositeResources
from ScoutSuite.providers.do.resources.kubernetes.kubernetes import Kubernetes


class Kubernetes(DoCompositeResources):
    _children = [(Kubernetes, "kubernetes")]

    def __init__(self, facade: DoFacade):
        super().__init__(facade)
        self.service = "kubernetes"

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
