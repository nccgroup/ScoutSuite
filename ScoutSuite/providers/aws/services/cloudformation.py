# -*- coding: utf-8 -*-

import json
import re

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


########################################
# CloudFormationRegionConfig
########################################

class CloudFormationRegionConfig(RegionConfig):
    """
    CloudFormation configuration for a single AWS region
    """
    stacks = {}

    def parse_stack(self, global_params, region, stack):
        """
        Parse a single stack and fetch additional attributes

        :param stack:
        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        """
        stack['id'] = stack.pop('StackId')
        stack['name'] = stack.pop('StackName')

        stack_description = api_clients[region].describe_stacks(StackName=stack['name'])
        stack['termination_protection'] = stack_description['Stacks'][0]['EnableTerminationProtection']
        stack['drifted'] = stack.pop('DriftInformation')['StackDriftStatus'] == 'DRIFTED'

        template = api_clients[region].get_template(StackName=stack['name'])['TemplateBody']
        stack['deletion_policy'] = self.has_deletion_policy(template)

        stack_policy = api_clients[region].get_stack_policy(StackName=stack['name'])
        if 'StackPolicyBody' in stack_policy:
            stack['policy'] = json.loads(stack_policy['StackPolicyBody'])
        self.stacks[stack['name']] = stack

    @staticmethod
    def has_deletion_policy(template):
        """
            Return region to be used for global calls such as list bucket and get bucket location

            :param template:                    The api response containing the stack's template
            :return:
            """
        has_dp = True
        # If a ressource is found to not have a deletion policy or have it to delete, the boolean is switched to
        # false to indicate that the ressource will be deleted once the stack is deleted
        if isinstance(template, dict):
            template = template['Resources']
            for group in template.keys():
                if 'DeletionPolicy' in template[group]:
                    if template[group]['DeletionPolicy'] is 'Delete':
                        has_dp = False
                else:
                    has_dp = False
        if isinstance(template, str):
            if re.match(r'\"DeletionPolicy\"\s*:\s*\"Delete\"', template):
                has_dp = False
            elif not re.match(r'\"DeletionPolicy\"', template):
                has_dp = False
        return has_dp


########################################
# CloudFormationConfig
########################################

class CloudFormationConfig(RegionalServiceConfig):
    """
    CloudFormation configuration for all AWS regions
    """

    region_config_class = CloudFormationRegionConfig

    def __init__(self, service_metadata, thread_config=4):
        super(CloudFormationConfig, self).__init__(service_metadata, thread_config)
