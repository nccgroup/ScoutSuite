from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade


class LoadBalancers(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):
        load_balancers = await self.facade.networking.get_load_balancers()
        if load_balancers:
            for load_balancer in load_balancers:
                id, load_balancer = await self._parse_load_balancer(load_balancer)
                self[id] = load_balancer

    async def _parse_load_balancer(self, raw_load_balancer):
        load_balancer_dict = {}

        load_balancer_dict["id"] = raw_load_balancer["id"]
        load_balancer_dict["name"] = raw_load_balancer["name"]
        load_balancer_dict["name"] = raw_load_balancer["name"]
        load_balancer_dict["redirect_http_to_https"] = str(
            raw_load_balancer["redirect_http_to_https"]
        )
        load_balancer_dict["enable_backend_keepalive"] = str(
            raw_load_balancer["enable_backend_keepalive"]
        )
        load_balancer_dict["droplet_ids"] = str(raw_load_balancer["droplet_ids"])
        return load_balancer_dict["id"], load_balancer_dict
