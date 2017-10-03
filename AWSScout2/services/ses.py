# -*- coding: utf-8 -*-

import json

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients



########################################
# SESRegionConfig
########################################

class SESRegionConfig(RegionConfig):
    """
    SES configuration for a single AWS region
    """

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
        dkim = api_clients[region].get_identity_dkim_attributes(Identities = [ identity_name ])['DkimAttributes'][identity_name]
        identity['DkimEnabled'] = dkim['DkimEnabled']
        identity['DkimVerificationStatus'] = dkim['DkimVerificationStatus']
        self.identities[self.get_non_aws_id(identity_name)] = identity



########################################
# SESConfig
########################################

class SESConfig(RegionalServiceConfig):
    """
    SES configuration for all AWS regions
    """

    region_config_class = SESRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(SESConfig, self).__init__(service_metadata, thread_config)
