from ScoutSuite.providers.aws.resources.ec2.ami import AmazonMachineImages
from ScoutSuite.providers.aws.resources.ec2.snapshots import Snapshots
from ScoutSuite.providers.aws.resources.ec2.volumes import Volumes
from ScoutSuite.providers.aws.resources.ec2.vpcs import Ec2Vpcs
from ScoutSuite.providers.aws.resources.regions import Regions


class EC2(Regions):
    _children = [
        (Ec2Vpcs, 'vpcs'),
        (AmazonMachineImages, 'images'),
        (Snapshots, 'snapshots'),
        (Volumes, 'volumes')
    ]

    def __init__(self, facade):
        super(EC2, self).__init__('ec2', facade)

    async def fetch_all(self, regions=None, excluded_regions=None, partition_name='aws', **kwargs):
        await super(EC2, self).fetch_all(regions, excluded_regions, partition_name)

        for region in self['regions']:
            self['regions'][region]['instances_count'] =\
                sum([len(vpc['instances']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['security_groups_count'] =\
                sum([len(vpc['security_groups']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['network_interfaces_count'] =\
                sum([len(vpc['network_interfaces']) for vpc in self['regions'][region]['vpcs'].values()])
        
        self['instances_count'] =\
            sum([region['instances_count'] for region in self['regions'].values()])
        self['security_groups_count'] =\
            sum([region['security_groups_count'] for region in self['regions'].values()])
        self['network_interfaces_count'] =\
            sum([region['network_interfaces_count'] for region in self['regions'].values()])
