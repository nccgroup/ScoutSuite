from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Clusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_clusters = await self.facade.elasticache.get_clusters(self.region, self.vpc)
        parsing_error_counter = 0
        for raw_cluster in raw_clusters:
            try:
                name, resource = self._parse_cluster(raw_cluster)
                self[name] = resource
            except Exception as e:
                parsing_error_counter += 1
        if parsing_error_counter > 0:
            print_exception(
                'Failed to parse {} resource: {} times'.format(self.__class__.__name__, parsing_error_counter))

    def _parse_cluster(self, raw_cluster):
        raw_cluster['name'] = raw_cluster.pop('CacheClusterId')
        raw_cluster['arn'] = 'arn:aws:elasticache:{}:{}:cluster/{}'.format(self.region,
                                                                             self.facade.owner_id,
                                                                             raw_cluster.get('name'))
        return raw_cluster['name'], raw_cluster
