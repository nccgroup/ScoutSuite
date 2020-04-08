import abc

from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.aws.facade.base import AWSFacade


class Regions(AWSCompositeResources, metaclass=abc.ABCMeta):
    def __init__(self, service: str, facade: AWSFacade):
        super(Regions, self).__init__(facade)
        self.service = service

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='aws', **kwargs):
        self['regions'] = {}
        for region in await self.facade.build_region_list(self.service, regions, excluded_regions, partition_name):
            self['regions'][region] = {
                'id': region,
                'region': region,
                'name': region
            }

        await self._fetch_children_of_all_resources(
            resources=self['regions'],
            scopes={region: {'region': region} for region in self['regions']}
        )

        self._set_counts()

    def _set_counts(self):
        self['regions_count'] = len(self['regions'])
        for _, key in self._children:
            # VPCs should not be counted as resources. They exist whether you have resources or not, so
            # counting them would make the report confusing.
            if key == 'vpcs':
                continue
                
            self[key + '_count'] = sum([region[key + '_count'] for region in self['regions'].values()])
