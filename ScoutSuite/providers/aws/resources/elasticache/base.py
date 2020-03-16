from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.elasticache.parametergroups import ParameterGroups
from ScoutSuite.providers.aws.resources.elasticache.securitygroups import SecurityGroups
from ScoutSuite.providers.aws.resources.elasticache.vpcs import ElastiCacheVpcs
from ScoutSuite.providers.aws.resources.regions import Regions


class ElastiCache(Regions):
    _children = [
        (ElastiCacheVpcs, 'vpcs'),
        (SecurityGroups, 'security_groups'),
        (ParameterGroups, 'parameter_groups')
    ]

    def __init__(self, facade: AWSFacade):
        super(ElastiCache, self).__init__('elasticache', facade)

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='aws', **kwargs):
        await super(ElastiCache, self).fetch_all(regions, excluded_regions, partition_name)

        for region in self['regions']:
            self['regions'][region]['clusters_count'] = \
                sum([len(vpc['clusters']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['subnet_groups_count'] = \
                sum([len(vpc['subnet_groups']) for vpc in self['regions'][region]['vpcs'].values()])
        
        self['clusters_count'] = sum([region['clusters_count'] for region in self['regions'].values()])

        # We do not want the parameter groups to be part of the resources count, as it is usually in 
        # the three of four digits and would make the resources count confusing.
        self.pop('parameter_groups_count')
