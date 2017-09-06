# -*- coding: utf-8 -*-
"""
ELBv2-related classes and functions
"""

from opinel.utils.aws import handle_truncated_response
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from AWSScout2.utils import ec2_classic, get_keys



########################################
# ELBv2RegionConfig
########################################

class ELBv2RegionConfig(RegionConfig):
    """
    ELBv2 configuration for a single AWS region

    :ivar vpcs:                         Dictionary of VPCs [id]
    """

    def __init__(self):
        self.vpcs = {}


    def parse_lb(self, global_params, region, lb):
        """

        :param global_params:
        :param region:
        :param source:
        :return:
        """
        lb['arn'] = lb.pop('LoadBalancerArn')
        lb['name'] = lb.pop('LoadBalancerName')
        vpc_id = lb.pop('VpcId') if 'VpcId' in lb and lb['VpcId'] else ec2_classic
        manage_dictionary(self.vpcs, vpc_id, ELBv2VPCConfig())
        lb['security_groups'] = []
        for sg in lb['SecurityGroups']:
            lb['security_groups'].append({'GroupId': sg})
        lb.pop('SecurityGroups')
        lb['listeners'] = {}
        # Get listeners
        listeners = handle_truncated_response(api_clients[region].describe_listeners, {'LoadBalancerArn': lb['arn']}, ['Listeners'])['Listeners']
        for listener in listeners:
            listener.pop('ListenerArn')
            listener.pop('LoadBalancerArn')
            port = listener.pop('Port')
            lb['listeners'][port] = listener
        # Get attributes
        lb['attributes'] = api_clients[region].describe_load_balancer_attributes(LoadBalancerArn = lb['arn'])['Attributes']
        # TOD: describe_ssl_policies


        self.vpcs[vpc_id].lbs[self.get_non_aws_id(lb['name'])] = lb



########################################
# ELBv2Config
########################################

class ELBv2Config(RegionalServiceConfig):
    """
    ELBv2 configuration for all AWS regions

    :cvar targets:                      Tuple with all ELBv2 resource names that may be fetched
    :cvar config_class:                 Class to be used when initiating the service's configuration in a new region/VPC
    """
    targets = (
        ('lbs', 'LoadBalancers', 'describe_load_balancers', {}, False),
    )
    region_config_class = ELBv2RegionConfig



########################################
# ELBv2VPCConfig
########################################

class ELBv2VPCConfig(object):
    """
    ELBv2 configuration for a single VPC

    :ivar flow_logs:                    Dictionary of flow logs [id]
    :ivar instances:                    Dictionary of instances [id]
    """

    def __init__(self, name = None):
        self.name = name
        self.lbs = {}
