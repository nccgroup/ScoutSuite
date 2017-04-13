# -*- coding: utf-8 -*-

import json

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# CloudFormationRegionConfig
########################################

class CloudFormationRegionConfig(RegionConfig):
    """
    CloudFormation configuration for a single AWS region

    :ivar stacks:                       Dictionary of stacks [name]
    :ivar stacks_count:                 Number of stacks in the region
    """

    def __init__(self):
        self.stacks = {}
        self.stacks_count = 0


    def parse_stack(self, global_params, region, stack):
        """
        Parse a single stack and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param stack_url:               URL of the AWS stack
        """
        stack['id'] = stack.pop('StackId')
        stack['name'] = stack.pop('StackName')
        stack_policy = api_clients[region].get_stack_policy(StackName = stack['name'])
        if 'StackPolicyBody' in stack_policy:
            stack['policy'] = json.loads(stack_policy['StackPolicyBody'])
        self.stacks[stack['name']] = stack



########################################
# CloudFormationConfig
########################################

class CloudFormationConfig(RegionalServiceConfig):
    """
    CloudFormation configuration for all AWS regions

    :cvar targets:                      Tuple with all CloudFormation resource names that may be fetched
    :cvar region_config_class:          Class to be used when initiating the service's configuration in a new region
    """
    targets = (
        ('stacks', 'Stacks', 'describe_stacks', False),
    )
    region_config_class = CloudFormationRegionConfig
