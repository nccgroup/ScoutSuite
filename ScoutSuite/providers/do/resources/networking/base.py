from ScoutSuite.providers.do.facade.base import DoFacade
from ScoutSuite.providers.do.resources.base import DoCompositeResources
from ScoutSuite.providers.do.resources.networking.firewalls import Firewalls
from ScoutSuite.providers.do.resources.networking.domains import Domains
from ScoutSuite.providers.do.resources.networking.load_balancers import LoadBalancers


class Networking(DoCompositeResources):
    _children = [
        (Firewalls, "firewalls"),
        (Domains, "domains"),
        (LoadBalancers, "load_balancers"),
    ]

    def __init__(self, facade: DoFacade):
        super().__init__(facade)
        self.service = "networking"

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
