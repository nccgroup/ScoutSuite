from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources, AWSResources


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


class EMRVpcs(AWSCompositeResources):
    _children = [
        (EMRClusters, 'clusters')
    ]

    def __init__(self, facade: AWSFacade, region: str):
        self.region = region

        super(EMRVpcs, self).__init__(facade)

    async def fetch_all(self):
        # EMR won't disclose its VPC, so we put everything in a VPC named "EMR-UNKNOWN-VPC", and we
        # infer the VPC afterwards during the preprocessing.
        tmp_vpc = 'EMR-UNKNOWN-VPC'
        self[tmp_vpc] = {}
        await self._fetch_children(self[tmp_vpc], {'region': self.region})


class EMR(Regions):
    _children = [
        (EMRVpcs, 'vpcs')
    ]

    def __init__(self, facade: AWSFacade):
        super(EMR, self).__init__('emr', facade)

    async def fetch_all(self, regions=None, partition_name='aws'):
        await super(EMR, self).fetch_all(regions, partition_name)

        for region in self['regions']:
            self['regions'][region]['clusters_count'] = sum(
                [len(vpc['clusters']) for vpc in self['regions'][region]['vpcs'].values()])

        self['clusters_count'] = sum(
            [region['clusters_count'] for region in self['regions'].values()])
