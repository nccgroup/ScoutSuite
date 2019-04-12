from ScoutSuite.providers.aws.resources.base import AWSResources


class Clusters(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_clusters = await self.facade.redshift.get_clusters(self.scope['region'], self.scope['vpc'])
        for raw_cluster in raw_clusters:
            id, cluster = self._parse_cluster(raw_cluster)
            self[id] = cluster

    def _parse_cluster(self, raw_cluster):
        name = raw_cluster.pop('ClusterIdentifier')
        raw_cluster['name'] = name

        return name, raw_cluster
