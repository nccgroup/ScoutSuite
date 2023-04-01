from ScoutSuite.providers.ksyun.resources.base import KsyunResources
from ScoutSuite.providers.ksyun.facade.base import KsyunFacade


class Clusters(KsyunResources):
    def __init__(self, facade: KsyunFacade, region: str):
        super().__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_clusters = await self.facade.kcs.get_clusters(region=self.region)
        if raw_clusters:
            for raw_cluster in raw_clusters:
                id, cluster = await self._parse_cluster(raw_cluster)
                self[id] = cluster

    async def _parse_cluster(self, raw_cluster):

        cluster_dict = {}

        cluster_dict['id'] = raw_cluster.get('InstanceId')


        return cluster_dict['id'], cluster_dict
