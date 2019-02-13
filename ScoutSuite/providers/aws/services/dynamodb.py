# -*- coding: utf-8 -*-

import json

from ScoutSuite.providers.aws.configs.regions import RegionalServiceConfig, RegionConfig, api_clients


########################################
# DynamoDBRegionConfig
########################################

class DynamoDBRegionConfig(RegionConfig):
    """
    DynamoDB configuration for a single AWS region
    """

    def parse_stack(self, global_params, region, table):
        """
        Parse a single table and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        """


########################################
# DynamoDBConfig
########################################

class DynamoDBConfig(RegionalServiceConfig):
    """
    DynamoDBConfig configuration for all AWS regions
    """

    region_config_class = DynamoDBRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(DynamoDBRegionConfig, self).__init__(service_metadata, thread_config)
