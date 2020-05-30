from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.regions import Regions

from .vpcs import EMRVpcs


class EMR(Regions):
    _children = [
        (EMRVpcs, 'vpcs')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('emr', facade)

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='aws', **kwargs):
        await super().fetch_all(regions, excluded_regions, partition_name)

        for region in self['regions']:
            self['regions'][region]['clusters_count'] = sum(
                [len(vpc['clusters']) for vpc in self['regions'][region]['vpcs'].values()])

        self['clusters_count'] = sum(
            [region['clusters_count'] for region in self['regions'].values()])
