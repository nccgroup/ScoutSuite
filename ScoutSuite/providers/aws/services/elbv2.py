# -*- coding: utf-8 -*-
"""
ELBv2-related classes and functions
"""

from opinel.utils.aws import handle_truncated_response
from opinel.utils.globals import manage_dictionary

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from ScoutSuite.providers.aws.configs.vpc import VPCConfig
from ScoutSuite.utils import ec2_classic


########################################
# ELBv2RegionConfig
########################################

class ELBv2RegionConfig(RegionConfig):
    """
    ELBv2 configuration for a single AWS region

    :ivar vpcs:                         Dictionary of VPCs [id]
    """

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
        manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
        lb['security_groups'] = []
        try:
            for sg in lb['SecurityGroups']:
                lb['security_groups'].append({'GroupId': sg})
            lb.pop('SecurityGroups')
        except Exception as e:
            # Network load balancers do not have security groups
            pass
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
        self.vpcs[vpc_id].lbs[self.get_non_provider_id(lb['name'])] = lb

    def parse_ssl_policie(self, global_params, region, policy):
        id = self.get_non_provider_id(policy['Name'])
        self.ssl_policies[id] = policy


########################################
# ELBv2Config
########################################

class ELBv2Config(RegionalServiceConfig):
    """
    ELBv2 configuration for all AWS regions
    """
    region_config_class = ELBv2RegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(ELBv2Config, self).__init__(service_metadata, thread_config)
