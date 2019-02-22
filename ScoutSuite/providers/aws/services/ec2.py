from ScoutSuite.providers.base.configs.resources import Resources
from ScoutSuite.providers.aws.configs.regions_config import RegionsConfig, ScopedResources
from ScoutSuite.providers.aws.facade import AWSFacade

from opinel.utils.aws import get_name
from ScoutSuite.utils import get_keys, ec2_classic


class EC2(RegionsConfig):
    def __init__(self):
        super(EC2, self).__init__('ec2')

    # TODO: Remove the credentials parameter. We had to keep it for compatibility
    async def fetch_all(self, credentials=None, regions=None, partition_name='aws'):
        await super(EC2, self).fetch_all(chosen_regions=regions, partition_name=partition_name)

        for region in self['regions']:
            self['regions'][region] = await Vpcs().fetch_all(region)


class Vpcs(ScopedResources):
    def __init__(self):
        self.facade = AWSFacade()
        super(Vpcs, self).__init__('vpcs')

    async def fetch_all(self, region):
        await super(Vpcs, self).fetch_all(region)

        for vpc in self['vpcs']:
            # TODO: Add vpc_resource_types
            instances = await EC2Instances(region).fetch_all(vpc)
            self['vpcs'][vpc].update(instances)

        self['instances_count'] = sum([vpc['instances_count'] for vpc in self['vpcs'].values()])

        return self

    def parse_resource(self, vpc):
        return vpc['VpcId'], vpc

    async def get_resources_in_scope(self, region):
        return self.facade.get_vpcs(region)


class EC2Instances(ScopedResources):
    def __init__(self, region):
        self.region = region
        self.facade = AWSFacade()
        super(EC2Instances, self).__init__('instances')

    def parse_resource(self, raw_instance):
        instance = {}
        #instance['reservation_id'] = reservation['ReservationId']
        id = raw_instance['InstanceId']
        instance['id'] = id
        instance['monitoring_enabled'] = raw_instance['Monitoring']['State'] == 'enabled'
        instance['user_data'] = self.facade.get_ec2_instance_user_data(
            self.region, id)

        # TODO: Those methods are slightly sketchy in my opinion (get methods which set stuff in a dictionary, say what)
        get_name(raw_instance, instance, 'InstanceId')
        get_keys(raw_instance, instance, ['KeyName', 'LaunchTime', 'InstanceType', 'State', 'IamInstanceProfile', 'SubnetId'])

        instance['network_interfaces'] = {}
        for eni in raw_instance['NetworkInterfaces']:
            nic = {}
            get_keys(eni, nic, ['Association', 'Groups', 'PrivateIpAddresses', 'SubnetId', 'Ipv6Addresses'])
            instance['network_interfaces'][eni['NetworkInterfaceId']] = nic

        return id, instance

    async def get_resources_in_scope(self, vpcs): 
        return self.facade.get_ec2_instances(self.region, vpcs)

class EC2Images(ScopedResources):
    def __init__(self, region):
        self.region = region
        self.facade = AWSFacade()
        super(EC2Images, self).__init__('images')
    
    async def get_resources_in_scope(self, vpcs): 
        return self.facade.get_ec2_instances(self.region, vpcs)

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
# # Globals
# ########################################

# icmp_message_types_dict = load_data('icmp_message_types.json', 'icmp_message_types')
# protocols_dict = load_data('protocols.json', 'protocols')


# ########################################
# # EC2RegionConfig
# ########################################

# class EC2RegionConfig(RegionConfig):
#     """
#     EC2 configuration for a single AWS region
#     """

#     def parse_elastic_ip(self, global_params, region, eip):
#         """

#         :param global_params:
#         :param region:
#         :param eip:
#         :return:
#         """
#         self.elastic_ips[eip['PublicIp']] = eip

#     def parse_instance(self, global_params, region, reservation):
#         """
#         Parse a single EC2 instance

#         :param global_params:           Parameters shared for all regions
#         :param region:                  Name of the AWS region
#         :param instance:                Cluster
#         """
#         for i in reservation['Instances']:
#             instance = {}
#             vpc_id = i['VpcId'] if 'VpcId' in i and i['VpcId'] else ec2_classic
#             manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
#             instance['reservation_id'] = reservation['ReservationId']
#             instance['id'] = i['InstanceId']
#             instance['monitoring_enabled'] = i['Monitoring']['State'] == 'enabled'
#             instance['user_data'] = self._get_user_data(region, instance['id'])
#             get_name(i, instance, 'InstanceId')
#             get_keys(i, instance, ['KeyName', 'LaunchTime', 'InstanceType', 'State', 'IamInstanceProfile', 'SubnetId'])
#             # Network interfaces & security groups
#             manage_dictionary(instance, 'network_interfaces', {})
#             for eni in i['NetworkInterfaces']:
#                 nic = {}
#                 get_keys(eni, nic, ['Association', 'Groups', 'PrivateIpAddresses', 'SubnetId', 'Ipv6Addresses'])
#                 instance['network_interfaces'][eni['NetworkInterfaceId']] = nic
#             self.vpcs[vpc_id].instances[i['InstanceId']] = instance

#     def _get_user_data(self, region, instance_id):
#         user_data_response = api_clients[region].describe_instance_attribute(Attribute='userData', InstanceId=instance_id)

#         if 'Value' not in user_data_response['UserData'].keys():
#             return None

#         return base64.b64decode(user_data_response['UserData']['Value']).decode('utf-8')

#     def parse_image(self, global_params, region, image):
#         """
#         Parses a single AMI (Amazon Machine Image)

#         :param global_params:           Parameters shared for all regions
#         :param region:                  Name of the AWS region
#         :param snapshot:                Single image
#         """
#         id = image['ImageId']
#         name = image['Name']

#         image['id'] = id
#         image['name'] = name

#         self.images[id] = image

#     def parse_security_group(self, global_params, region, group):
#         """
#         Parse a single Redsfhit security group

#         :param global_params:           Parameters shared for all regions
#         :param region:                  Name of the AWS region
#         :param security)_group:         Security group
#         """
#         vpc_id = group['VpcId'] if 'VpcId' in group and group['VpcId'] else ec2_classic
#         manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
#         security_group = {}
#         security_group['name'] = group['GroupName']
#         security_group['id'] = group['GroupId']
#         security_group['description'] = group['Description']
#         security_group['owner_id'] = group['OwnerId']
#         security_group['rules'] = {'ingress': {}, 'egress': {}}
#         security_group['rules']['ingress']['protocols'], security_group['rules']['ingress'][
#             'count'] = self.__parse_security_group_rules(group['IpPermissions'])
#         security_group['rules']['egress']['protocols'], security_group['rules']['egress'][
#             'count'] = self.__parse_security_group_rules(group['IpPermissionsEgress'])
#         self.vpcs[vpc_id].security_groups[group['GroupId']] = security_group

#     def __parse_security_group_rules(self, rules):
#         """

#         :param self:
#         :param rules:
#         :return:
#         """
#         protocols = {}
#         rules_count = 0
#         for rule in rules:
#             ip_protocol = rule['IpProtocol'].upper()
#             if ip_protocol == '-1':
#                 ip_protocol = 'ALL'
#             protocols = manage_dictionary(protocols, ip_protocol, {})
#             protocols[ip_protocol] = manage_dictionary(protocols[ip_protocol], 'ports', {})
#             # Save the port (single port or range)
#             port_value = 'N/A'
#             if 'FromPort' in rule and 'ToPort' in rule:
#                 if ip_protocol == 'ICMP':
#                     # FromPort with ICMP is the type of message
#                     port_value = icmp_message_types_dict[str(rule['FromPort'])]
#                 elif rule['FromPort'] == rule['ToPort']:
#                     port_value = str(rule['FromPort'])
#                 else:
#                     port_value = '%s-%s' % (rule['FromPort'], rule['ToPort'])
#             manage_dictionary(protocols[ip_protocol]['ports'], port_value, {})
#             # Save grants, values are either a CIDR or an EC2 security group
#             for grant in rule['UserIdGroupPairs']:
#                 manage_dictionary(protocols[ip_protocol]['ports'][port_value], 'security_groups', [])
#                 protocols[ip_protocol]['ports'][port_value]['security_groups'].append(grant)
#                 rules_count = rules_count + 1
#             for grant in rule['IpRanges']:
#                 manage_dictionary(protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
#                 protocols[ip_protocol]['ports'][port_value]['cidrs'].append({'CIDR': grant['CidrIp']})
#                 rules_count = rules_count + 1
#             # IPv6
#             for grant in rule['Ipv6Ranges']:
#                 manage_dictionary(protocols[ip_protocol]['ports'][port_value], 'cidrs', [])
#                 protocols[ip_protocol]['ports'][port_value]['cidrs'].append({'CIDR': grant['CidrIpv6']})
#                 rules_count = rules_count + 1

#         return protocols, rules_count

#     def parse_snapshot(self, global_params, region, snapshot):
#         """

#         :param global_params:           Parameters shared for all regions
#         :param region:                  Name of the AWS region
#         :param snapshot:                  Single snapshot
#         :return:
#         """
#         snapshot['id'] = snapshot.pop('SnapshotId')
#         snapshot['name'] = get_name(snapshot, snapshot, 'id')
#         self.snapshots[snapshot['id']] = snapshot
#         # Get snapshot attribute
#         snapshot['createVolumePermission'] = \
#         api_clients[region].describe_snapshot_attribute(Attribute='createVolumePermission', SnapshotId=snapshot['id'])[
#             'CreateVolumePermissions']
#         snapshot['public'] = self._is_public(snapshot)

#     def _is_public(self, snapshot):
#         return any([permission.get('Group') == 'all' for permission in snapshot['createVolumePermission']])

#     def parse_volume(self, global_params, region, volume):
#         """

#         :param global_params:           Parameters shared for all regions
#         :param region:                  Name of the AWS region
#         :param volume:                  Single EBS volume
#         :return:
#         """
#         volume['id'] = volume.pop('VolumeId')
#         volume['name'] = get_name(volume, volume, 'id')
#         self.volumes[volume['id']] = volume


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


# def manage_vpc(vpc_info, vpc_id):
#     """
#     Ensure name and ID are set

#     :param vpc_info:
#     :param vpc_id:
#     :return:
#     """
#     manage_dictionary(vpc_info, vpc_id, {})
#     vpc_info[vpc_id]['id'] = vpc_id
#     if not 'name' in vpc_info[vpc_id]:
#         vpc_info[vpc_id]['name'] = vpc_id
