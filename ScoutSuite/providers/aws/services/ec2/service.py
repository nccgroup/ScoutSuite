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
        
            


# # -*- coding: utf-8 -*-
# """
# EC2-related classes and functions
# """

# # TODO: move a lot of this to VPCconfig, and use some sort of filter to only list SGs in EC2 classic
# import netaddr
# import base64

# from opinel.utils.aws import get_name
# from opinel.utils.console import printException, printInfo
# from opinel.utils.fs import load_data
# from opinel.utils.globals import manage_dictionary

# from ScoutSuite.providers.aws.configs.vpc import VPCConfig
# from ScoutSuite.providers.base.configs.browser import get_attribute_at
# from ScoutSuite.providers.base.provider import BaseProvider
# from ScoutSuite.utils import get_keys, ec2_classic
# from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


# ########################################
# # EC2RegionConfig
# ########################################

# class EC2RegionConfig(RegionConfig):
#     """
#     EC2 configuration for a single AWS region
#     """

# ########################################
# # EC2Config
# ########################################

# class EC2Config(RegionalServiceConfig):
#     """
#     EC2 configuration for all AWS regions
#     """

#     region_config_class = EC2RegionConfig

#     def __init__(self, service_metadata, thread_config=4):
#         super(EC2Config, self).__init__(service_metadata, thread_config)


# ########################################
# ##### EC2 analysis functions
# ########################################

# def analyze_ec2_config(ec2_info, aws_account_id, force_write):
#     try:
#         printInfo('Analyzing EC2 config... ', newLine=False)
#         # Custom EC2 analysis
#         #        check_for_elastic_ip(ec2_info)
#         # FIXME - commented for now as this method doesn't seem to be defined anywhere'
#         # list_network_attack_surface(ec2_info, 'attack_surface', 'PublicIpAddress')
#         # TODO: make this optional, commented out for now
#         # list_network_attack_surface(ec2_info, 'private_attack_surface', 'PrivateIpAddress')
#         printInfo('Success')
#     except Exception as e:
#         printInfo('Error')
#         printException(e)

# def add_security_group_name_to_ec2_grants_callback(ec2_config, current_config, path, current_path, ec2_grant,
#                                                    callback_args):
#     """
#     Callback

#     :param ec2_config:
#     :param current_config:
#     :param path:
#     :param current_path:
#     :param ec2_grant:
#     :param callback_args:
#     :return:
#     """
#     sg_id = ec2_grant['GroupId']
#     if sg_id in current_path:
#         target = current_path[:(current_path.index(sg_id) + 1)]
#         ec2_grant['GroupName'] = get_attribute_at(ec2_config, target, 'name')
#     elif ec2_grant['UserId'] == callback_args['AWSAccountId']:
#         if 'VpcId' in ec2_grant:
#             target = current_path[:(current_path.index('vpcs') + 1)]
#             target.append(ec2_grant['VpcId'])
#             target.append('security_groups')
#             target.append(sg_id)
#         else:
#             target = current_path[:(current_path.index('security_groups') + 1)]
#             target.append(sg_id)
#         ec2_grant['GroupName'] = get_attribute_at(ec2_config, target, 'name')


# def check_for_elastic_ip(ec2_info):
#     """
#     Check that the whitelisted EC2 IP addresses are not static IPs

#     :param ec2_info:
#     :return:
#     """
#     # Build a list of all elatic IP in the account
#     elastic_ips = []
#     for region in ec2_info['regions']:
#         if 'elastic_ips' in ec2_info['regions'][region]:
#             for eip in ec2_info['regions'][region]['elastic_ips']:
#                 elastic_ips.append(eip)
#     new_items = []
#     new_macro_items = []
#     for i, item in enumerate(ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].items):
#         ip = netaddr.IPNetwork(item)
#         found = False
#         for eip in elastic_ips:
#             eip = netaddr.IPNetwork(eip)
#             if ip in eip:
#                 found = True
#                 break
#         if not found:
#             new_items.append(ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].items[i])
#             new_macro_items.append(ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].macro_items[i])
#     ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].items = new_items
#     ec2_info['violations']['non-elastic-ec2-public-ip-whitelisted'].macro_items = new_macro_items


# def link_elastic_ips_callback2(ec2_config, current_config, path, current_path, instance_id, callback_args):
#     if instance_id == callback_args['instance_id']:
#         if not 'PublicIpAddress' in current_config:
#             current_config['PublicIpAddress'] = callback_args['elastic_ip']
#         elif current_config['PublicIpAddress'] != callback_args['elastic_ip']:
#             printInfo('Warning: public IP address exists (%s) for an instance associated with an elastic IP (%s)' % (
#             current_config['PublicIpAddress'], callback_args['elastic_ip']))
#             # This can happen... fix it


# def list_instances_in_security_groups(region_info):
#     """
#     Once all the data has been fetched, iterate through instances and list them
#     Could this be done when all the "used_by" values are set ??? TODO

#     :param region_info:
#     :return:
#     """
#     for vpc in region_info['vpcs']:
#         if not 'instances' in region_info['vpcs'][vpc]:
#             return
#         for instance in region_info['vpcs'][vpc]['instances']:
#             state = region_info['vpcs'][vpc]['instances'][instance]['State']['Name']
#             for sg in region_info['vpcs'][vpc]['instances'][instance]['security_groups']:
#                 sg_id = sg['GroupId']
#                 manage_dictionary(region_info['vpcs'][vpc]['security_groups'][sg_id], 'instances', {})
#                 manage_dictionary(region_info['vpcs'][vpc]['security_groups'][sg_id]['instances'], state, [])
#                 region_info['vpcs'][vpc]['security_groups'][sg_id]['instances'][state].append(instance)

