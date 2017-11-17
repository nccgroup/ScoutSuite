# -*- coding: utf-8 -*-
"""
Redshift-related classes and functions
"""

from opinel.utils.aws import handle_truncated_response
from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from AWSScout2.configs.vpc import VPCConfig
from AWSScout2.utils import ec2_classic


########################################
# RedshiftRegionConfig
########################################

class RedshiftRegionConfig(RegionConfig):
    """
    Redshift configuration for a single AWS region
    """

    def parse_cluster(self, global_params, region, cluster):
        """
        Parse a single Redshift cluster

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param cluster:                 Cluster
        """
        vpc_id = cluster.pop('VpcId') if 'VpcId' in cluster else ec2_classic
        manage_dictionary(self.vpcs, vpc_id, VPCConfig(self.vpc_resource_types))
        name = cluster.pop('ClusterIdentifier')
        cluster['name'] = name
        self.vpcs[vpc_id].clusters[name] = cluster


    def parse_parameter_group(self, global_params, region, parameter_group):
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


    def parse_security_group(self, global_params, region, security_group):
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
    """

    region_config_class = RedshiftRegionConfig

    def __init__(self, service_metadata, thread_config = 4):
        super(RedshiftConfig, self).__init__(service_metadata, thread_config)
