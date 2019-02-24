from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.aws.configs.regions_config import Regions, ScopedResources
from ScoutSuite.providers.aws.services.ec2.ami import AmazonMachineImages
from ScoutSuite.providers.aws.services.ec2.vpcs import Vpcs
from ScoutSuite.providers.aws.services.ec2.snapshots import Snapshots
from ScoutSuite.providers.aws.services.ec2.volumes import Volumes

from opinel.utils.aws import get_aws_account_id
from ScoutSuite.utils import get_keys, ec2_classic


# TODO: Add docstrings

class EC2(Regions):
    def __init__(self):
        super(EC2, self).__init__('ec2')

    async def fetch_all(self, credentials=None, regions=None, partition_name='aws'):
        await super(EC2, self).fetch_all(chosen_regions=regions, partition_name=partition_name)

        # TODO: Is there a way to generalize this? 
        for region in self['regions']:
            self['regions'][region]['vpcs'] = await Vpcs().fetch_all(region)
            self['regions'][region]['instances_count'] = sum([vpc['instances'].count for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['security_groups_count'] = sum([vpc['security_groups'].count for vpc in self['regions'][region]['vpcs'].values()])
            self['regions'][region]['network_interfaces_count'] = sum([vpc['network_interfaces'].count for vpc in self['regions'][region]['vpcs'].values()])

            self['regions'][region]['images'] = await AmazonMachineImages(get_aws_account_id(credentials)).fetch_all(region)
            self['regions'][region]['images_count'] = self['regions'][region]['images'].count

            self['regions'][region]['snapshots'] = await Snapshots(get_aws_account_id(credentials)).fetch_all(region)
            self['regions'][region]['snapshots_count'] = self['regions'][region]['snapshots'].count
            
            self['regions'][region]['volumes'] = await Volumes().fetch_all(region)
            self['regions'][region]['volumes_count'] = self['regions'][region]['volumes'].count