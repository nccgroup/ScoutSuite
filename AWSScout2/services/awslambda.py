# -*- coding: utf-8 -*-
"""
Lambda-related classes and functions
"""

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig



########################################
# LambdaRegionConfig
########################################

class LambdaRegionConfig(RegionConfig):

    pass



########################################
# LambdaConfig
########################################

class LambdaConfig(RegionalServiceConfig):
    """
    Lambda configuration for all AWS regions
    """

    region_config_class = LambdaRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(LambdaConfig, self).__init__(service_metadata, thread_config)
