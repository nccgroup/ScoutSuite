# -*- coding: utf-8 -*-
"""
ELB-related classes and functions
"""
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from AWSScout2.utils import ec2_classic, get_keys



########################################
# ELBRegionConfig
########################################

class ELBRegionConfig(RegionConfig):
    """
    ELB configuration for a single AWS region

    :ivar vpcs:                         Dictionary of VPCs [id]
    """

    def __init__(self):
        self.vpcs = {}
        self.elb_policies = {}

    def parse_elb(self, global_params, region, lb):
        """

        :param global_params:
        :param region:
        :param elb:
        :return:
        """
        elb = {}
        elb['name'] = lb.pop('LoadBalancerName')
        vpc_id = lb['VPCId'] if 'VPCId' in lb and lb['VPCId'] else ec2_classic
        manage_dictionary(self.vpcs, vpc_id, ELBVPCConfig())
        get_keys(lb, elb, ['DNSName', 'CreatedTime', 'AvailabilityZones', 'Subnets', 'Scheme'])
        elb['security_groups'] = []
        for sg in lb['SecurityGroups']:
            elb['security_groups'].append({'GroupId': sg})
        manage_dictionary(elb, 'listeners', {})
        policy_names = []
        for l in lb['ListenerDescriptions']:
            listener = l['Listener']
            manage_dictionary(listener, 'policies', [])
            for policy_name in l['PolicyNames']:
                policy_id = self.get_non_aws_id(policy_name)
                listener['policies'].append(policy_id)
                if policy_id not in self.elb_policies:
                    policy_names.append(policy_name)
            elb['listeners'][l['Listener']['LoadBalancerPort']] = listener
        # Fetch LB policies here. This is not ideal, but the alternative is to download all policies and clean up after...
        if len(policy_names):
            policies = api_clients[region].describe_load_balancer_policies(LoadBalancerName = elb['name'], PolicyNames = policy_names)['PolicyDescriptions']
            for policy in policies:
                policy['name'] = policy.pop('PolicyName')
                policy_id = self.get_non_aws_id(policy['name'])
                self.elb_policies[policy_id] = policy
        manage_dictionary(elb, 'instances', [])
        for i in lb['Instances']:
            elb['instances'].append(i['InstanceId'])
        self.vpcs[vpc_id].elbs[self.get_non_aws_id(elb['name'])] = elb



########################################
# ELBConfig
########################################

class ELBConfig(RegionalServiceConfig):
    """
    ELB configuration for all AWS regions

    :cvar targets:                      Tuple with all ELB resource names that may be fetched
    :cvar config_class:                 Class to be used when initiating the service's configuration in a new region/VPC
    """
    targets = (
        ('elbs', 'LoadBalancerDescriptions', 'describe_load_balancers', {}, False),
    )
    region_config_class = ELBRegionConfig

    def finalize(self):
        pass



########################################
# ELBVPCConfig
########################################

class ELBVPCConfig(object):
    """
    ELB configuration for a single VPC

    :ivar flow_logs:                    Dictionary of flow logs [id]
    :ivar instances:                    Dictionary of instances [id]
    """

    def __init__(self, name = None):
        self.name = name
        self.elbs = {}
