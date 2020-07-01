from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources


class Clusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_clusters = await self.facade.redshift.get_clusters(self.region, self.vpc)
        for raw_cluster in raw_clusters:
            id, cluster = self._parse_cluster(raw_cluster)
            self[id] = cluster

    def _parse_cluster(self, raw_cluster):
        name = raw_cluster.pop('ClusterIdentifier')
        raw_cluster['name'] = name
        raw_cluster['arn'] = 'arn:aws:redshift:{}:{}:cluster/{}'.format(self.region,
                                                                    self.facade.owner_id,
                                                                    name)

        return name, raw_cluster
