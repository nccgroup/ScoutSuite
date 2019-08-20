from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class EMRClusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str):
        super(EMRClusters, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_clusters = await self.facade.emr.get_clusters(self.region)
        for raw_cluster in raw_clusters:
            name, resource = self._parse_cluster(raw_cluster)
            self[name] = resource

    def _parse_cluster(self, raw_cluster):
        raw_cluster['id'] = raw_cluster.pop('Id')
        raw_cluster['name'] = raw_cluster.pop('Name')
        return raw_cluster['id'], raw_cluster
