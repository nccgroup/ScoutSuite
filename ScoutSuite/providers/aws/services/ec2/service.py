from ScoutSuite.providers.aws.resources.resources import Regions
from ScoutSuite.providers.aws.services.ec2.ami import AmazonMachineImages
from ScoutSuite.providers.aws.services.ec2.vpcs import Vpcs
from ScoutSuite.providers.aws.services.ec2.snapshots import Snapshots
from ScoutSuite.providers.aws.services.ec2.volumes import Volumes

from opinel.utils.aws import get_aws_account_id
from ScoutSuite.utils import get_keys, ec2_classic


# TODO: Add docstrings

class EC2(Regions):
    children = [
        (Vpcs, 'vpcs'),
        (AmazonMachineImages, 'images'),
        (Snapshots, 'snapshots'),
        (Volumes, 'volumes')
    ]

    def __init__(self):
        super(EC2, self).__init__('ec2')

    async def fetch_all(self, credentials=None, regions=None, partition_name='aws'):
        await super(EC2, self).fetch_all(credentials, regions, partition_name)

        for region in self['regions']:
            # TODO: Is there a way to move this elsewhere? 
            self['regions'][region]['instances_count'] = sum([len(vpc['instances']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['security_groups_count'] = sum([len(vpc['security_groups']) for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['network_interfaces_count'] = sum([len(vpc['network_interfaces']) for vpc in self['regions'][region]['vpcs'].values()])
        
        self['instances_count'] = sum([region['instances_count'] for region in self['regions'].values()])
        self['security_groups_count'] = sum([region['security_groups_count'] for region in self['regions'].values()])
        self['network_interfaces_count'] = sum([region['network_interfaces_count'] for region in self['regions'].values()])
