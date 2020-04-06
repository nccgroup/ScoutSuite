from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.rds.parametergroups import ParameterGroups
from ScoutSuite.providers.aws.resources.rds.securitygroups import SecurityGroups
from ScoutSuite.providers.aws.resources.rds.vpcs import RDSVpcs
from ScoutSuite.providers.aws.resources.regions import Regions


class RDS(Regions):
    _children = [
        (RDSVpcs, 'vpcs'),
        (ParameterGroups, 'parameter_groups'),
        (SecurityGroups, 'security_groups')
    ]

    def __init__(self, facade: AWSFacade):
        super(RDS, self).__init__('rds', facade)

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='aws', **kwargs):
        await super(RDS, self).fetch_all(regions, excluded_regions, partition_name)

        for region in self['regions']:
            self['regions'][region]['instances_count'] =\
                sum([len(vpc['instances']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['snapshots_count'] =\
                sum([len(vpc['snapshots']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['subnet_groups_count'] =\
                sum([len(vpc['subnet_groups']) for vpc in self['regions'][region]['vpcs'].values()])
        
        self['instances_count'] = sum([region['instances_count'] for region in self['regions'].values()])
        self['snapshots_count'] = sum([region['snapshots_count'] for region in self['regions'].values()])
        self['subnet_groups_count'] = sum([region['subnet_groups_count'] for region in self['regions'].values()])
