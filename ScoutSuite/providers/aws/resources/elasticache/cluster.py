from ScoutSuite.providers.aws.resources.base import AWSResources


class Clusters(AWSResources):
    async def fetch_all(self, **kwargs):
        raw_clusters = await self.facade.elasticache.get_clusters(self.scope['region'], self.scope['vpc'])
        for raw_cluster in raw_clusters:
            name, resource = self._parse_cluster(raw_cluster)
            self[name] = resource

    def _parse_cluster(self, raw_cluster):
        raw_cluster['name'] = raw_cluster.pop('CacheClusterId')
        return raw_cluster['name'], raw_cluster
