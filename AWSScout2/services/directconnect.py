# -*- coding: utf-8 -*-

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig



########################################
# DirectConnectRegionConfig
########################################

class DirectConnectRegionConfig(RegionConfig):
    """
    DirectConnect configuration for a single AWS region

    :ivar connections:                       Dictionary of connections [name]
    :ivar connections_count:                 Number of connections in the region
    """

    def __init__(self):
        self.connections = {}
        self.connections_count = 0


    def parse_connection(self, global_params, region, connection_url):
        """
        Parse a single connection and fetch additional attributes

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param connection_url:               URL of the AWS connection
        """
        connection['id'] = connection.pop('connectionId')
        connection['name'] = connection.pop('connectionName')
        self.connections[connection['id']] = connection



########################################
# DirectConnectConfig
########################################

class DirectConnectConfig(RegionalServiceConfig):
    """
    DirectConnect configuration for all AWS regions

    :cvar targets:                      Tuple with all DirectConnect resource names that may be fetched
    :cvar region_config_class:          Class to be used when initiating the service's configuration in a new region
    """
    targets = (
        ('connections', 'connections', 'describe_connections', False),
    )
    region_config_class = DirectConnectRegionConfig
