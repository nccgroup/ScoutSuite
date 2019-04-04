import abc

from ScoutSuite.providers.aws.utils import get_aws_account_id
from ScoutSuite.providers.aws.resources.base import AWSCompositeResources
from ScoutSuite.providers.aws.facade.base import AWSFacade


class Regions(AWSCompositeResources, metaclass=abc.ABCMeta):
    def __init__(self, service: str, facade: AWSFacade):
        self.service = service
        self.facade = facade

    async def fetch_all(self, credentials, regions=None, partition_name='aws'):
        self['regions'] = {}
        account_id = get_aws_account_id(credentials)
        for region in await self.facade.build_region_list(self.service, regions, partition_name):
            self['regions'][region] = {
                'id': region,
                'region': region,
                'name': region
            }

        await self._fetch_children_of_all_resources(
            resources=self['regions'],
            scopes={region: {'region': region, 'owner_id': account_id} for region in self['regions']}
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
