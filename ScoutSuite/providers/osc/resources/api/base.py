from ScoutSuite.providers.osc.resources.api.securitygroups import SecurityGroups
from ScoutSuite.providers.osc.resources.regions import Regions
from ScoutSuite.providers.osc.resources.api.snapshots import Snapshots
from ScoutSuite.providers.osc.resources.api.volumes import Volumes


class API(Regions):
    _children = [
        (SecurityGroups, 'security_groups'),
        (Snapshots, 'snapshots'),
        #(Volumes, 'volumes')
    ]

    def __init__(self, facade):
        super(API, self).__init__('api', facade)

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='osc', **kwargs):
        await super(API, self).fetch_all(regions, excluded_regions)
        for region in self['regions']:
            self['regions'][region]['security_groups_count'] =\
                sum([len(sg) for sg in self['regions'][region]['security_groups'].values()])
        self['security_groups_count'] = sum([region['security_groups_count'] for region in self['regions'].values()])
