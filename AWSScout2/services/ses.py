# -*- coding: utf-8 -*-

import json

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# SESRegionConfig
########################################

class SESRegionConfig(RegionConfig):
    """
    SES configuration for a single AWS region

    :ivar identities:                       Dictionary of identities [name]
    :ivar identities_count:                 Number of identities in the region
    """

    def __init__(self):
        self.identities = {}
        self.identities_count = 0


    def parse_identitie(self, global_params, region, identity_name):
        """
        Parse a single identity and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        """
        identity = {'name': identity_name, 'policies': {}}
        policy_names = api_clients[region].list_identity_policies(Identity = identity_name)['PolicyNames']
        if len(policy_names):
            policies = api_clients[region].get_identity_policies(Identity = identity_name, PolicyNames = policy_names)['Policies']
            for policy_name in policies:
                identity['policies'][policy_name] = json.loads(policies[policy_name])
        self.identities[self.get_non_aws_id(identity_name)] = identity



########################################
# SESConfig
########################################

class SESConfig(RegionalServiceConfig):
    """
    SES configuration for all AWS regions

    :cvar targets:                      Tuple with all SES resource names that may be fetched
    :cvar region_config_class:          Class to be used when initiating the service's configuration in a new region
    """
    targets = (
        ('identities', 'Identities', 'list_identities', False),
    )
    region_config_class = SESRegionConfig