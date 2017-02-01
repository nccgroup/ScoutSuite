# -*- coding: utf-8 -*-
"""
Redshift-related classes and functions
"""

# Import AWSScout2
from AWSScout2.configs import RegionalServiceConfig, RegionConfig, api_clients
from AWSScout2.utils import handle_truncated_response



########################################
# RedshiftRegionConfig
########################################

class RedshiftRegionConfig(RegionConfig):
    """
    Redshift configuration for a single AWS region

    :ivar queues:                       Dictionary of queues [name]
    :ivar queues_count:                 Number of queues in the region
    """

    def __init__(self):
        self.clusters = {}
        self.clusters_count = 0
        self.parameter_groups = {}
        self.parameter_groups_count = 0
        self.security_groups = {}
        self.security_groups_count = 0


    def _fetch_cluster(self, global_params, region, cluster):
        """
        Parse a single Redshift cluster

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param cluster:                 Cluster
        """
        vpc_id = cluster.pop('VpcId') if 'VpcId' in cluster else ec2_classic
        manage_dictionary(region_config['vpcs'], vpc_id, {})
        manage_dictionary(region_config['vpcs'][vpc_id], 'clusters', {})
        name = cluster.pop('ClusterIdentifier')
        cluster['name'] = name
        self.clusters[name] = cluster

    def _fetch_parameter_group(self, global_params, region, parameter_group):
        """
        Parse a single Redshift parameter group and fetch all of its parameters

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param parameter_group:         Parameter group
        """
        pg_name = parameter_group.pop('ParameterGroupName')
        pg_id = self.get_non_aws_id(pg_name) # Name could be used as only letters digits or hyphens
        parameter_group['name'] = pg_name
        parameter_group['parameters'] = {}
        api_client = api_clients[region]
        parameters = handle_truncated_response(api_client.describe_cluster_parameters, {'ParameterGroupName': pg_name}, ['Parameters'])['Parameters']
        for parameter in parameters:
            param = {}
            param['value'] = parameter['ParameterValue']
            param['source'] = parameter['Source']
            parameter_group['parameters'][parameter['ParameterName']] = param
        (self).parameter_groups[pg_id] = parameter_group

    def _fetch_security_group(self, global_params, region, security_group):
        """
        Parse a single Redsfhit security group

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param security)_group:         Security group
        """
        name = security_group.pop('ClusterSecurityGroupName')
        security_group['name'] = name
        self.security_groups['name'] = security_group



########################################
# RedshiftConfig
########################################

class RedshiftConfig(RegionalServiceConfig):
    """
    Redshift configuration for all AWS regions

    :cvar targets:                      Tuple with all Redshift resource names that may be fetched
    :cvar region_config_class:          Class to be used when initiating the service's configuration in a new region
    """
    targets = (
        ('clusters', 'Clusters', 'describe_clusters', False),
        ('parameter_groups', 'ParameterGroups', 'describe_cluster_parameter_groups', False),
        ('security_groups', 'SecurityGroups', 'describe_cluster_security_groups', True),
    ) # TODO: add support for Redshift subnet groups?
    region_config_class = RedshiftRegionConfig
