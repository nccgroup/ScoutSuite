from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.config.recorders import Recorders
from ScoutSuite.providers.aws.resources.config.rules import Rules
from ScoutSuite.providers.aws.resources.regions import Regions


class Config(Regions):
    _children = [
        (Recorders, 'recorders'),
        (Rules, 'rules')
    ]

    def __init__(self, facade: AWSFacade):
        super(Config, self).__init__('config', facade)

    async def fetch_all(self, regions=None, partition_name='aws'):
        await super(Config, self).fetch_all(regions, partition_name)

        for region in self['regions']:
            config_enabled = any(recorder['config_enabled']
                                 for recorder in self['regions'][region]['recorders'].values())
            self['regions'][region]['config_enabled'] = config_enabled
            self['regions'][region]['regions_count'] = 1
