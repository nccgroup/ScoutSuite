from ScoutSuite.providers.base.configs.resources import SimpleResources
from ScoutSuite.providers.base.configs.resources import CompositeResources
from ScoutSuite.providers.aws.facade.facade import AWSFacade
from opinel.utils.aws import get_aws_account_id
import abc

class AWSSimpleResources(SimpleResources, metaclass=abc.ABCMeta):
    def __init__(self, scope):
        self.scope = scope
        self.facade = AWSFacade()

    async def fetch_all(self):
        raw_resources = await self.get_resources_from_api()
        for raw_resource in raw_resources:
            name, resource = self.parse_resource(raw_resource)
            self[name] = resource

class AWSCompositeResources(CompositeResources, metaclass=abc.ABCMeta):

    # TODO: get rid of the credentials.
    async def fetch_children(self, parent, **kwargs):
        for child_class, key in self.children:
            child = child_class(**kwargs)
            await child.fetch_all()
            if parent.get(key) is None: 
                parent[key] = {}
            parent[key].update(child)
            parent[key + '_count'] = len(child)

class Regions(AWSCompositeResources, metaclass=abc.ABCMeta):
    def __init__(self, service):
        self.service = service
        # TODO: Should be injected
        self.facade = AWSFacade()

    async def fetch_all(self, credentials, chosen_regions=None, partition_name='aws'):
        self['regions'] = {}
        for region in await self.facade.build_region_list(self.service, chosen_regions, partition_name):
            # TODO: Do we really need id, region AND name? 
            self['regions'][region] = {
                'id': region,
                'region': region,
                'name': region
            }

            await self.fetch_children(self['regions'][region], scope={'region': region, 'owner_id': get_aws_account_id(credentials)})

        self._set_counts()

    def _set_counts(self):
        self['regions_count'] = len(self['regions'])
        for _, key in self.children:
            self[key + '_count'] = sum([region[key + '_count'] for region in self['regions'].values()])
