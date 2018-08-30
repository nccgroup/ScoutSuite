# -*- coding: utf-8 -*-
"""
ELB-related classes and functions
"""
from opinel.utils.globals import manage_dictionary

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from ScoutSuite.providers.aws.configs.vpc import VPCConfig
from ScoutSuite.utils import ec2_classic, get_keys



########################################
# ELBRegionConfig
########################################

class ELBRegionConfig(RegionConfig):
    """
    ELB configuration for a single AWS region
    """

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
        manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
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
                policy_id = self.get_non_provider_id(policy_name)
                listener['policies'].append(policy_id)
                if policy_id not in self.elb_policies:
                    policy_names.append(policy_name)
            elb['listeners'][l['Listener']['LoadBalancerPort']] = listener
        # Fetch LB policies here. This is not ideal, but the alternative is to download all policies and clean up after...
        if len(policy_names):
            policies = api_clients[region].describe_load_balancer_policies(LoadBalancerName = elb['name'], PolicyNames = policy_names)['PolicyDescriptions']
            for policy in policies:
                policy['name'] = policy.pop('PolicyName')
                policy_id = self.get_non_provider_id(policy['name'])
                self.elb_policies[policy_id] = policy
        manage_dictionary(elb, 'instances', [])
        for i in lb['Instances']:
            elb['instances'].append(i['InstanceId'])
        # Get attributes
        elb['attributes'] = api_clients[region].describe_load_balancer_attributes(LoadBalancerName=elb['name'])['LoadBalancerAttributes']
        self.vpcs[vpc_id].elbs[self.get_non_provider_id(elb['name'])] = elb



########################################
# ELBConfig
########################################

class ELBConfig(RegionalServiceConfig):
    """
    ELB configuration for all AWS regions
    """

    region_config_class = ELBRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(ELBConfig, self).__init__(service_metadata, thread_config)
