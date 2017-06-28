# -*- coding: utf-8 -*-

from opinel.utils.globals import manage_dictionary

from AWSScout2.configs.regions import RegionalServiceConfig, RegionConfig, api_clients
from AWSScout2.utils import ec2_classic



########################################
# ElastiCacheRegionConfig
########################################

class ElastiCacheRegionConfig(RegionConfig):
    """
    ElastiCache configuration for a single AWS region

    :ivar vpcs:                         Dictionary of VPCs [id]
    :ivar clusters_count:               Number of clusters in the region
    :ivar security_groups:              Dictionary of security groups [name]
    :ivar security_groups_count:        Number of security groups in the region
    """

    def __init__(self):
        self.vpcs = {}
        self.clusters_count = 0
        self.parameter_groups = {}
        self.parameter_groups_count = 0
        self.security_groups = {}
        self.security_groups_count = 0


    def parse_cluster(self, global_params, region, cluster):
        """
        Parse a single ElastiCache cluster

        :param global_params:           Parameters shared for all regions
        :param region:                  Name of the AWS region
        :param cluster:                 ElastiCache cluster
        """
        cluster_name = cluster.pop('CacheClusterId')
        cluster['name'] = cluster_name
        # Must fetch info about the subnet group to retrieve the VPC ID...
        if 'CacheSubnetGroupName' in cluster:
            subnet_group = api_clients[region].describe_cache_subnet_groups(CacheSubnetGroupName = cluster['CacheSubnetGroupName'])['CacheSubnetGroups'][0]
            vpc_id = subnet_group['VpcId']
        else:
            vpc_id = ec2_classic
            subnet_group = None
        manage_dictionary(self.vpcs, vpc_id, ElastiCacheVPCConfig())
        self.vpcs[vpc_id].clusters[cluster_name] = cluster
        if subnet_group:
            self.vpcs[vpc_id].subnet_groups[subnet_group['CacheSubnetGroupName']] = subnet_group


    def parse_security_group(self, global_params, region, security_group):
        """
        Parse a single ElastiCache security group

        :param global_params:
        :param region:
        :param security_group:
        :return:
        """
        security_group['name'] = security_group.pop('CacheSecurityGroupName')
        self.security_groups[security_group['name']] = security_group



########################################
# ElastiCacheConfig
########################################

class ElastiCacheConfig(RegionalServiceConfig):
    """
    ElastiCache configuration for all AWS regions

    :cvar targets:                      Tuple with all ElastiCache resource names that may be fetched
    :cvar config_class:                 Class to be used when initiating the service's configuration in a new region/VPC
    """
    targets = (
        ('clusters', 'CacheClusters', 'describe_cache_clusters', {}, False),
        ('security_groups', 'CacheSecurityGroups', 'describe_cache_security_groups', {}, True)      # Do not throw errors as this is disabled in newer regions
        #('parameter_groups', 'DBParameterGroups', 'describe_db_parameter_groups', False),
    )
    region_config_class = ElastiCacheRegionConfig



########################################
# ElastiCacheVPCConfig
########################################

class ElastiCacheVPCConfig(object):
    """
    ElastiCache configuration for a single VPC

    :ivar clusters:                     Dictionary of clusters [name]
    :ivar subnet_groups:                Dictionary of subnet groups [name]
    """

    def __init__(self):
        self.clusters = {}
        self.subnet_groups = {}
