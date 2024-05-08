from ScoutSuite.providers.do.resources.base import DoResources
from ScoutSuite.providers.do.facade.base import DoFacade


class Kubernetes(DoResources):
    def __init__(self, facade: DoFacade):
        super().__init__(facade)

    async def fetch_all(self):
        clusters = await self.facade.kubernetes.get_kubernetes()
        if clusters:
            for cluster in clusters:
                id, cluster = await self._parse_cluster(cluster)
                self[id] = cluster

    async def _parse_cluster(self, raw_cluster):
        cluster_dict = {}

        cluster_dict["id"] = raw_cluster["id"]
        cluster_dict["name"] = raw_cluster["name"]
        cluster_dict["ha"] = raw_cluster["ha"]
        cluster_dict["auto_upgrade"] = raw_cluster["auto_upgrade"]
        cluster_dict["surge_upgrade"] = raw_cluster["surge_upgrade"]

        return cluster_dict["id"], cluster_dict
